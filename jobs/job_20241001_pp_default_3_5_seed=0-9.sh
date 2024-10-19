#!/bin/bash
for n_data_samples in "400"
do
    for model in "Lotka_Volterra" #"Lotka_Volterra" "Lorenz" "SIR" "Fluid_Flow"
    do
        for seed in {0..9}
        do
            for loss_method in "VF"
            do 
                for noise_ratio in "0.20" #"0.000" "0.001" "0.002" "0.004" "0.008" "0.016" "0.032" "0.064" "0.128" "0.256" "0.512" "1.024"
                do
                    for n_dynamic in "default_3"
                    do
                        timestring=$(taskset -c 16-63 python shell_timestring.py)
                        output_path="outputs/${model}_${timestring}.txt"
                        taskset -c 16-63 echo "python -u make_datasets.py --task ${model} --num_env 5 --use_new_reward 0 --loss_func ${loss_method} --num_run 10 --noise_ratio ${noise_ratio} --seed ${seed} --task_ode_num -1 --transplant_step 500 --eta 0.9999  --combine_operator average --n_dynamic ${n_dynamic} --timestring ${timestring} --n_data_samples ${n_data_samples} >> ${output_path}"
                        taskset -c 16-63 python -u make_datasets.py --task ${model} --num_env 5 --use_new_reward 0 --loss_func ${loss_method} --num_run 10 --noise_ratio ${noise_ratio} --seed ${seed} --task_ode_num -1 --transplant_step 500 --eta 0.9999  --combine_operator average --n_dynamic ${n_dynamic} --timestring ${timestring} --n_data_samples ${n_data_samples} >> ${output_path}
                        ipad_data_path="data/${model}/${timestring}/dump/data.pkl" 
                        for eq_id in "1" "2"
                        do
                            for env_id in "0" "1" "2" "3" "4"
                            do
                                timestring=$(taskset -c 16-63 python shell_timestring.py)
                                taskset -c 16-63 echo "python -u run_dcode.py --x_id ${eq_id} --basis=sine --n_basis=50 --env_id=${env_id} --load_ipad_data=${ipad_data_path} --timestring ${timestring} 2>&1 | tee -a ${output_path} >> ${output_path}"
                                taskset -c 16-63 python -u run_dcode.py --x_id ${eq_id} --basis=sine --n_basis=50 --env_id=${env_id} --load_ipad_data=${ipad_data_path} --timestring ${timestring} 2>&1 | tee -a ${output_path}
                            done
                        done
                    done
                done
            done
        done
    done
done
