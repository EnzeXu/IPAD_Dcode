ode_name=Lotka_Volterra
n_dynamic=default_1
noise_ratio=0.00
seed=0

timestring=$(python shell_timestring.py)
output_path="outputs/${ode_name}_${timestring}.txt"
echo "python -u make_datasets.py --task ${ode_name} --num_env 5 --use_new_reward 0 --loss_func L2 --num_run 10 --noise_ratio ${noise_ratio} --seed ${seed} --task_ode_num -1 --transplant_step 500 --eta 0.9999  --combine_operator average --n_dynamic ${n_dynamic} --timestring ${timestring} --n_data_samples 400 >> ${output_path}"
python -u make_datasets.py --task ${ode_name} --num_env 5 --use_new_reward 0 --loss_func L2 --num_run 10 --noise_ratio ${noise_ratio} --seed ${seed} --task_ode_num -1 --transplant_step 500 --eta 0.9999  --combine_operator average --n_dynamic ${n_dynamic} --timestring ${timestring} --n_data_samples 400 >> ${output_path}
ipad_data_path="data/${ode_name}/${timestring}/dump/data.pkl"

for eq_id in {1..2}
do
    for env_id in {0..4}
    do
        timestring=$(python shell_timestring.py)
        echo "python -u run_dcode.py --x_id ${eq_id} --basis=sine --n_basis=50 --env_id=${env_id} --load_ipad_data=${ipad_data_path} --timestring ${timestring} 2>&1 | tee -a ${output_path} >> ${output_path}"
        python -u run_dcode.py --x_id ${eq_id} --basis=sine --n_basis=50 --env_id=${env_id} --load_ipad_data=${ipad_data_path} --timestring ${timestring} 2>&1 | tee -a ${output_path}
    done
done

#
#n_basis=50
#
#save_dir=results_test
#mkdir -p ${save_dir}
#test_folder=data.pkl
#
#for env in $(seq 0 4)
#do
#    echo "python -u run_sensitivity_vi.py --basis=sine --n_basis=${n_basis} --n_sample=1 --env=${env} --save_dir=${save_dir} --load_ipad_data=${test_folder} 2>&1 | tee -a ${save_dir}/ipad.txt"
#    python -u run_sensitivity_vi.py --basis=sine --n_basis=${n_basis} --n_sample=1 --env=${env} --save_dir=${save_dir} --load_ipad_data=${test_folder} 2>&1 | tee -a ${save_dir}/ipad.txt
#    # exit
#done
#
#
