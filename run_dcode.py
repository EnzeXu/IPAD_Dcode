import sympy
import argparse
import numpy as np

import equations
import data
from gp_utils import run_gp_ode
from interpolate import get_ode_data
import pickle
import os
import time
import basis

import datetime
import os
import pandas as pd
import pytz
import sys

from invariant_physics.dataset import simplify_and_replace_constants, judge_expression_equal, extract

current_dir = os.getcwd()
sys.path.insert(0, os.path.join(current_dir, 
                                'Invariant_Physics'))


def get_now_string(time_string="%Y%m%d_%H%M%S_%f"):
    # return datetime.datetime.now().strftime(time_string)
    est = pytz.timezone('America/New_York')

    # Get the current time in UTC and convert it to EST
    utc_now = datetime.datetime.utcnow().replace(tzinfo=pytz.utc)
    est_now = utc_now.astimezone(est)

    # Return the time in the desired format
    return est_now.strftime(time_string)



def run(ode_name, ode_param, x_id, freq, n_sample, noise_ratio, seed, n_basis, basis_str, ipad_data, args, data_timestring, curve_names, ipad_args, ipad_params_config):
    log_start_time = args.timestring

    save_dir = args.save_dir
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    log_path = f"{save_dir}/{ipad_args.task}_end.csv"

    if not os.path.exists(log_path):
        with open(log_path, "a") as f:
            f.write(f"start_time,end_time,data_time,task,n_dynamic,task_ode_num,correct,noise_ratio,env_id,trajectory,time_cost,f_hat,f_true,cleaned_pred,cleaned_truth,match,seed\n")

    
    import pandas as pd
#     try:
#         # df = pd.read_csv(f"{save_dir}/summary_{args.dataset}.csv", header=None,
#         #                 names=['end_time', 'status', 'ODE', 'x_id', 'correct', 'noise', 'env_id', 'seed', "time_elapsed"]
#         #                 )
#         df = pd.read_csv(f"{save_dir}/summary_{args.dataset}.csv")
#         # df = df[df["status"] == "End"]
#         df = df.astype({
#         #     'term_success_predicted_rate': 'float32',
#         #     'correct': 'bool',
#             'env_id': 'int32',
#             'seed': 'int32',
#             'x_id': 'float32',
#             'noise': 'float32',
#         })
#         df["correct"] = df["correct"].apply(lambda x: True if x=="True" else False)
#         current_entry = df[(df.seed==seed) & (df.env_id==args.env_id) & (df.x_id==x_id) & (df.noise==noise_ratio) & (df.n_dynamic==ipad_args.n_dynamic) &  (df["task"]==ode_name)]
#         if len(current_entry) == 0:
#             pass
#         else:
#             print(current_entry)
#             print("Entry already seen, skipping..")
#             return
#     except:
#         print("Can't find summary in", save_dir)
#         pass
    
    np.random.seed(seed)

    ode = equations.get_ode(ode_name, ode_param, args.env_id, data=ipad_data)
    T = ode.T
    init_low = 0
    init_high = ode.init_high

    if basis_str == 'sine':
        basis_obj = basis.FourierBasis
    else:
        basis_obj = basis.CubicSplineBasis

    noise_sigma = ode.std_base * noise_ratio  
    
    dg = data.DataGenerator(ode, ode_name, T, freq, n_sample, noise_sigma, init_low, init_high, False, args.env_id, seed=seed, dataset=ipad_args.n_dynamic)
    yts = dg.generate_data()
    
    for traj in range(yts.shape[0]):
        yt = yts[traj:traj+1, :, :]
        print("yt.shape", yt.shape)
        if ipad_data:
            t = ipad_data['t_series_list'][args.env_id]
        else:
            t = dg.solver.t[:yt.shape[0]]
        ode_data, X_ph, y_ph, t_new = get_ode_data(yt, x_id, t, dg, ode, n_basis, basis_obj,
                                                  env=args.env_id)

        # path_base = 'results_vi/{}/noise-{}/sample-{}/freq-{}/n_basis-{}/basis-{}'.\
        #     format(ode_name, noise_ratio, n_sample, freq, n_basis, basis_str)
        #
        # if not os.path.isdir(path_base):
        #     os.makedirs(path_base)

        # for s in range(seed, seed+1):
    #         print(' ')

        print('Running with seed {}'.format(seed))
        start = time.time()
    #         print(X_ph.shape, y_ph.shape, x_id)
    #         import pdb;pdb.set_trace()

        f_hat, est_gp = run_gp_ode(ode_data, X_ph, y_ph,  ode, x_id, seed)

        if ipad_data:
            f_true = ipad_data['params_config']['truth_ode_format'][x_id]
            correct = None
        else:
            f_true = ode.get_expression()[x_id]
            if not isinstance(f_true, tuple):
                correct = sympy.simplify(f_hat - f_true) == 0
            else:
                correct_list = [sympy.simplify(f_hat - f) == 0 for f in f_true]
                correct = max(correct_list) == 1
        print(f_hat, f_true)
#         import pdb;pdb.set_trace()
    #         print(correct_list)
        # results/${ode}/noise-${noise}-seed-${seed}-env-${env}.txt
        # s, f_hat, f_true, x_id

        log_end_time = get_now_string()
        end = time.time()

        f_true_clear = ipad_params_config['truth_ode_format'][x_id].format(*[1.0 for _ in range(len(ipad_params_config["random_params_base"]))])
        f_true_clear = simplify_and_replace_constants(f_true_clear)

#         f_hat_clear = str(f_hat)
#         for i_curve, one_curve_name in enumerate(curve_names):
#             f_hat_clear = f_hat_clear.replace(f"X{i_curve}", one_curve_name)
#         f_hat_clear = simplify_and_replace_constants(f_hat_clear)
        
        print("[Original expr:]", f_hat)
        f_hat = str(f_hat)
        for i_curve, one_curve_name in enumerate(curve_names):
            f_hat = f_hat.replace(f"X{i_curve}", one_curve_name)

        full_terms, terms, coefficient_terms = extract(f_hat)
        expr = " + ".join([str(item) for item in full_terms])
        print("[Before replacing constants:]", expr)
        f_hat_clear = simplify_and_replace_constants(expr)
        print("[After replacing constants:]", f_hat_clear)

        match = judge_expression_equal(f_true_clear, f_hat_clear)

        end_result_line = f"{log_start_time},{log_end_time},{data_timestring},{ode_name},{ipad_args.n_dynamic},{x_id},{correct},{noise_ratio:.3f},{args.env_id},{traj},{end-start},{f_hat},{f_true},{f_hat_clear},{f_true_clear},{match},{seed}\n"
        with open(log_path, "a") as f:
            f.write(end_result_line)
        print(end_result_line)
        # f.write(f"{log_end_time},truth,{str(f_true)}\n")
        # f.write(f"{log_end_time},prediction,{str(f_hat)}\n")

    # if x_id == 0:
    #     path = path_base + 'grad_seed_{}.pkl'.format(seed)
    # else:
    #     path = path_base + 'grad_x_{}_seed_{}.pkl'.format(x_id, seed)
    #

#         with open(path, 'wb') as f:
#             pickle.dump({
#                 'model': est_gp._program,
#                 'ode_data': ode_data,
#                 'seed': s,
#                 'correct': correct,
#                 'f_hat': f_hat,
#                 'ode': ode,
#                 'noise_ratio': noise_ratio,
#                 'noise_sigma': noise_sigma,
#                 'dg': dg,
#                 't_new': t_new,
#                 'time': end - start,
#             }, f)

    print(correct)
    print("="*30)


if __name__ == '__main__':
    command = " ".join(sys.argv)
    print(f"Command: {command}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--ode_name", help="name of the ode", type=str)
    parser.add_argument("--ode_param", help="parameters of the ode (default: None)", type=str, default=None)
    parser.add_argument("--x_id", help="ID of the equation to be learned", type=int, default=0)
    parser.add_argument("--freq", help="sampling frequency", type=float, default=10)
    # parser.add_argument("--n_sample", help="number of trajectories", type=int, default=100)
    # parser.add_argument("--noise_ratio", help="noise level (default 0)", type=float, default=0.)
    parser.add_argument("--n_basis", help="number of basis function", type=int, default=50)
    parser.add_argument("--basis", help="basis function", type=str, default='sine')

    # parser.add_argument("--seed", help="random seed", type=int, default=0)
    parser.add_argument("--env_id", help="random seed", type=int, default=-1) # 1
    # parser.add_argument("--dataset", help=" ", type=str, default="default_1")
    # parser.add_argument("--save_dir", help=" ", type=str, default="./result")
    parser.add_argument("--load_ipad_data", help=" ", type=str, default="")
    parser.add_argument("--timestring", help="timestring", type=str, default='20001111_222222_333333')
    
    args = parser.parse_args()
    print('Running with: ', args)

    if args.ode_param is not None:
        param = [float(x) for x in args.ode_param.split(',')]
    else:
        param = None
        
    if args.load_ipad_data:
        with open(args.load_ipad_data, 'rb') as file:
            ipad_data = pickle.load(file)
        ode_name = ipad_data['args'].task
        param = None
        # x_id = ipad_data['args'].task_ode_num - 1
        n_sample = -1
        noise_ratio = ipad_data['args'].noise_ratio
        seed = ipad_data['args'].seed
        data_timestring = ipad_data['args'].timestring
        curve_names = ipad_data["params_config"]["curve_names"]
        ipad_args = ipad_data['args']
        ipad_params_config = ipad_data["params_config"]
        args.save_dir = f"./logs/{ipad_args.task}/"
        args.x_id = args.x_id - 1
    else:
        # ode_name = args.ode_name
        # param = param
        # x_id = args.x_id
        # n_sample = args.n_sample
        # noise_ratio = args.noise_ratio
        # seed = args.seed
        # ipad_data = None
        # timestring = get_now_string()
        raise NotImplementedError

    
    run(ode_name, param, args.x_id, args.freq, n_sample, noise_ratio, seed, n_basis=args.n_basis, basis_str=args.basis, ipad_data=ipad_data, args=args, data_timestring=data_timestring, curve_names=curve_names, ipad_args=ipad_args, ipad_params_config=ipad_params_config)
    # python -u run_dcode.py --basis=sine --n_basis=50 --env_id=${env_id} --load_ipad_data=${test_folder} 2>&1 | tee -a outputs/${task}_${timestring}.txt