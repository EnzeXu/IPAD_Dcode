#!/bin/bash
for n_data_samples in "400"
do
    for model in "Friction_Pendulum" #"Lotka_Volterra" "Lorenz" "SIR" "Fluid_Flow"
    do
        for seed in {0..1}
        do
            for loss_method in "VF"
            do 
                for noise_ratio in "0.15" #"0.000" "0.001" "0.002" "0.004" "0.008" "0.016" "0.032" "0.064" "0.128" "0.256" "0.512" "1.024"
                do
                    for num_env in "5"
                    do
                        for n_dynamic in "default_0"
                        do
                            timestring=$(python shell_timestring.py)
                            output_path="outputs/${model}_${timestring}.txt"
                            echo "python -u make_datasets.py --task ${model} --num_env ${num_env} --use_new_reward 0 --loss_func ${loss_method} --num_run 10 --noise_ratio ${noise_ratio} --seed ${seed} --task_ode_num -1 --transplant_step 500 --eta 0.9999  --combine_operator average --n_dynamic ${n_dynamic} --timestring ${timestring} --n_data_samples ${n_data_samples} >> ${output_path}"
                            python -u make_datasets.py --task ${model} --num_env ${num_env} --use_new_reward 0 --loss_func ${loss_method} --num_run 10 --noise_ratio ${noise_ratio} --seed ${seed} --task_ode_num -1 --transplant_step 500 --eta 0.9999  --combine_operator average --n_dynamic ${n_dynamic} --timestring ${timestring} --n_data_samples ${n_data_samples} >> ${output_path}
                            ipad_data_path="data/${model}/${timestring}/dump/data.pkl"
                            for eq_id in "1" "2"
                            do
                                for env_id in "0" "1" "2" "3" "4"
                                do
                                    timestring=$(python shell_timestring.py)
                                    echo "python -u run_dcode.py --x_id ${eq_id} --basis=sine --n_basis=50 --env_id=${env_id} --load_ipad_data=${ipad_data_path} --timestring ${timestring} 2>&1 | tee -a ${output_path} >> ${output_path}"
                                    python -u run_dcode.py --x_id ${eq_id} --basis=sine --n_basis=50 --env_id=${env_id} --load_ipad_data=${ipad_data_path} --timestring ${timestring} 2>&1 | tee -a ${output_path}
                                done
                            done
                        done
                    done
                done

            done
        done
    done
done
