#========================================================
# Create some configs that we'll be using frequently
#Using dataclass and typing for safety: make sure we have the right number of arguments
# and the right type
"""
We can add some new configs and register those configs to be used in the future.
"""

#NO_REGISTRY_ERR = "Model {} not in MODEL_REGISTRY! Available models are {}"

#from dataclasses import dataclass
from typing import Any, Callable, Dict, List, NewType, Tuple

CONFIG_REGISTRY = {}


def RegisterConfig(name):
    """Registers a model."""

    def decorator(f):
        CONFIG_REGISTRY[name] = f
        return f
    return decorator

def create_config(config_name: str)-> dict:
    assert config_name in CONFIG_REGISTRY.keys(        
    ), "Unknown configuration"
    _config = CONFIG_REGISTRY[config_name]()
    assert isinstance(_config, dict)
    return _config

"""
@dataclass
class EncoderConfig:
    n_in: int
    n_out: int
    hidden_configuration: Tuple[str, int]

@dataclass
class DecoderConfig:
    n_in_decoder: int
    hidden_configuration_decoder: Tuple[str, int]
    n_out_decoder: Any = None  # Need to defined later 
                                #(depends on the task)
    window_size:  Any = None

@dataclass
class TransformerConfig:
    n_in_decoder: int
    hidden_configuration_decoder: Dict[str, int]
    n_out_transformer: int
    n_out_decoder: Any=None #Need to defined later
                            #(depends on the task)
    window_size: Any=None

@dataclass
class LINEARTransformConfig:
    target_intensity: Any = None
    target_intensity_cat: Any=None
    window_size: Any = None
    n_out_decoder: Any=None #Need to defined later
                            #(depends on the task)
"""

#=========================
# All our configs
#Enc.
@RegisterConfig('full_encoder_config')
def full_encoder_config():
    return dict(
    n_in=3 * 3,
    n_out=128,
    hidden_configuration=(
        ('conv', 64),
        ('conv', 64),
        ('maxpool', None),
        ('conv', 256),
        ('maxpool', None),
        ('flatten', 256 * 4 * 4),
        ('linear', 256),
        ('fc', 128)
    ))

@RegisterConfig('split_encoder_config')
def split_encoder_config():
    return dict(
    n_in=3,
    n_out=128,
    hidden_configuration=(
        ('conv', 64),
        ('conv', 64),
        ('maxpool', None),
        ('conv', 256),
        ('maxpool', None),
        ('flatten', 256 * 4 * 4),
        ('linear', 256),
        ('fc', 128)
    ))

#Dec.
@RegisterConfig('encdec_config')
def encdec_config():
    return dict(
    #out_cnn + number of stat
    n_in_decoder=128 + 10, 
    n_out_decoder=None, 
    hidden_configuration_decoder=(
        ('gru', 128),
        ('gru', 128)
    ))



#Dec.
@RegisterConfig('transformer_config')
def transformer_config(): 
    return dict(
        n_in=128+10,
        n_head=2,
        dim_feedforward=2048,
        num_layers=6,
        dropout=0.1,
        window_size=None,
        n_out_unroll=None,
        max_len_pe=10,
        pool_method='default',
        activation='tanh')

@RegisterConfig('transformer_config_noviz')
def transformer_config_noviz(): 
    return dict(
        n_in=10,
        n_head=2,
        dim_feedforward=512,
        num_layers=6,
        dropout=0.2,
        window_size=None,
        n_out_unroll=None,
        max_len_pe=10,
        pool_method='default',
        activation='tanh')

#Dec
@RegisterConfig('lstm_config')
def gru_config():
    return dict(
        n_in=128+10,
        hidden_dim=256,
        rnn_num_layers=2,
        N_OUT=128,
        rnn_type='gru',
        dropout=0.1,
        activation_fn='tanh',
        bidir=True)


@RegisterConfig('lineartransform_config')
def lineartransform_config():
    return dict()


