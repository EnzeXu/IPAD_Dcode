import basis


def get_config_real(x_id=0):
    return real_config


def get_config(ode, x_id=0):
    if ode.name == 'GompertzODE':
        if ode.has_coef:
            return gompertz_config
        else:
            return gompertz_config_no_coef
    elif ode.name == 'LogisticODE':
        return logistic_config
    elif ode.name == 'SelkovODE':
        return selkov_config
    elif ode.name == 'FracODE':
        return frac_config
    elif ode.name == 'Lorenz':
        if x_id == 0:
            return lorenz_config_x0
        elif x_id == 1:
            print('loading config for X1')
            return lorenz_config_x1
        else:
            print('loading config for X2')
            return lorenz_config_x2
    elif ode.name == 'LvODE':
        return lv_config
    elif ode.name == 'SirODE':
        return sir_config
    elif hasattr(ode, 'data'):
        if ode.name == "Lotka_Volterra":
            return ipad_lv_config
        elif ode.name == "SIR":
            return ipad_sir_config
        elif ode.name == "Lorenz":
            return ipad_lorenz_config
        elif ode.name == "Friction_Pendulum":
            return ipad_friction_pen_config
        else:
            return default_config
    else:
        return default_config


def get_interpolation_config(ode, x_id=0):
    if ode.name == 'GompertzODE':
        return gompertz_interp_config
    elif ode.name == 'Lorenz':
        if x_id == 0:
            return lorenz_interp_config
        else:
            return lorenz_interp_config2
    elif ode.name == 'LogisticODE':
        return logistic_interp_config
    elif ode.name == 'SelkovODE':
        return selkov_interp_config
    elif ode.name == 'real':
        return real_interp_config
    elif ode.name == 'FracODE':
        return frac_interp_config
    elif ode.name == 'LvODE':
        return lv_interp_config
    elif ode.name == 'SirODE':
        return sir_interp_config
    else:
        return default_interp_config
        # raise ValueError



gompertz_interp_config = {
    'r': 2,
    'sigma_in_mul': 2.,
    'freq_int': 20,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}

frac_interp_config = {
    'r': 7,
    'sigma_in': 0.01,
    'freq_int': 20,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.CubicSplineBasis,
}

real_interp_config = {
    'r': 4,
    'sigma_in': 0.15,
    'freq_int': 365*2,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}

logistic_interp_config = {
    'r': 3,
    'sigma_in_mul': 2.,
    'freq_int': 20,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}

lorenz_interp_config = {
    'r': -1,
    'sigma_in_mul': 2.,
    'freq_int': 100,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}

lorenz_interp_config2 = {
    'r': -1,
    'sigma_in': 0.1,
    'freq_int': 100,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}

selkov_interp_config = {
    'r': 2,
    'sigma_in': 0.2,
    'freq_int': 20,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}

lv_interp_config = {
    'r': 2,
    'sigma_in_mul': 0.15,
    'freq_int': 100,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}
sir_interp_config = {
    'r': 2,
    'sigma_in_mul': 0.15,
    'freq_int': 100,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}
default_interp_config = {
    'r': 2,
    'sigma_in_mul': 0.15,
    'freq_int': 100,
    'new_sample': 5,
    'n_basis': 50,
    'basis': basis.FourierBasis,
}

gompertz_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'neg': 1, 'mul': 3, 'log': 1, 'add': 1},
                   'const_range': (1, 2),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

frac_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'neg': 1, 'mul': 1, 'div': 1, 'add': 1},
                   'const_range': (1, 2),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': False,#True
                   }


real_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'neg': 1, 'mul': 3, 'log': 1, 'add': 1},
                   'const_range': (0, 10),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 1,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

logistic_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 1, 'pow': 1, 'add': 1},
                   'const_range': (1., 2.),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 1,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

selkov_config = {'population_size': 30000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 1, 'add': 1},
                   'const_range': (0.01, 1.),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 1,
                   'parsimony_coefficient': 0.001,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

gompertz_config_no_coef = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'neg': 1, 'mul': 3, 'log': 1, 'add': 1},
                   'const_range': None,
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

lorenz_config_x0 = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (0.001, 30),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

lorenz_config_x1 = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (25, 30),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

lorenz_config_x2 = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (1.1, 5),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

lv_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (0.005, 0.1),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }
sir_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (0.01, 4.0),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 0.9,
                   'verbose': 0,
                   'parsimony_coefficient': 0.01,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

default_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (0.01, 30.0),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 1.0,
                   'verbose': 0,
                   'parsimony_coefficient': 0.1,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

## IPAD configs
ipad_lv_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (0.01, 30.0),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 1.0,
                   'verbose': 0,
                   'parsimony_coefficient': 0.1,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

ipad_sir_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (0.005, 0.1),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 1.0,
                   'verbose': 0,
                   'parsimony_coefficient': 0.1,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

ipad_lorenz_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1},
                   'const_range': (2, 30),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 1.0,
                   'verbose': 0,
                   'parsimony_coefficient': 0.1,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }

ipad_friction_pen_config = {'population_size': 15000,
                   'p_crossover': 0.6903,
                   'p_subtree_mutation': 0.133,
                   'p_hoist_mutation': 0.0361,
                   'p_point_mutation': 0.0905,
                   'function_set': {'sub': 1, 'mul': 3, 'add': 1, 'sin': 3, 'div': 3},
                   'const_range': (0.5, 3.0),
                   'generations': 20,
                   'stopping_criteria': 0.01,
                   'max_samples': 1.0,
                   'verbose': 0,
                   'parsimony_coefficient': 0.1,
                   'init_depth': (1, 6),
                   'n_jobs': 2,
                   'low_memory': True
                   }



