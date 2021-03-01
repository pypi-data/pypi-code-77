import click
from .cmd_asap import asap
from .func_asap import *
from .cmd_cli_options import *

@asap.group('gen_desc')
@click.option('--stride', '-s',
                     help='Read in the xyz trajectory with X stide. Default: read/compute all frames.',
                     default=1)
@click.option('--periodic/--no-periodic', 
                     help='Is the system periodic? If not specified, will infer from the XYZ file.',
                     default=True)
@click.pass_context
@file_input_options
@file_output_options
def gen_desc(ctx, in_file, fxyz, prefix, stride, periodic):
    """
    Descriptor generation command
    This command function evaluated before the descriptor specific ones,
    we setup the general stuff here, such as read the files.
    """

    if not xyz and not in_file:
        return
        
    if in_file:
        # Here goes the routine to compute the descriptors according to the
        # state file(s)
        ctx.obj.update(load_in_file(in_file))

    if prefix is None: prefix = "ASAP-desc"
    if fxyz is not None:
        ctx.obj['data']['fxyz'] = fxyz
        ctx.obj['data']['stride'] = stride
        ctx.obj['data']['periodic'] = periodic
    ctx.obj['desc_options']['prefix'] = prefix

@gen_desc.command('soap')
@click.option('--cutoff', '-c', type=float, 
              help='Cutoff radius', 
              show_default=True, default=3.0)
@click.option('--nmax', '-n', type=int, 
              help='Maximum radial label', 
              show_default=True, default=6)
@click.option('--lmax', '-l', type=int, 
              help='Maximum angular label (<= 9)', 
              show_default=True, default=6)
@click.option('--rbf', type=click.Choice(['gto', 'polynomial'], case_sensitive=False), 
              help='Radial basis function', 
              show_default=True, default='gto')
@click.option('--atom-gaussian-width', '-sigma', '-g', type=float, 
              help='The width of the Gaussian centered on atoms.', 
              show_default=True, default=0.5)
@click.option('--crossover/--no-crossover', 
              help='If to included the crossover of atomic types.', 
              show_default=True, default=False)
@click.option('--universal_soap', '--usoap', '-u',
              type=click.Choice(['none','smart','minimal', 'longrange'], case_sensitive=False), 
              help='Try out our universal SOAP parameters.', 
              show_default=True, default='none')
@click.pass_context
@desc_options
@atomic_to_global_desc_options
def soap(ctx, tag, cutoff, nmax, lmax, atom_gaussian_width, crossover, rbf, universal_soap,
         kernel_type, zeta, element_wise, peratom):
    """Generate SOAP descriptors"""
    # load up the xyz
    ctx.obj['asapxyz'] = ASAPXYZ(ctx.obj['data']['fxyz'], ctx.obj['data']['stride'], ctx.obj['data']['periodic'])
 
    if universal_soap != 'none':
        from asaplib.hypers import universal_soap_hyper
        global_species = ctx.obj['asapxyz'].get_global_species()
        soap_spec = universal_soap_hyper(global_species, universal_soap, dump=True)
    else:
        soap_spec = {'soap1': {'type': 'SOAP',
                               'cutoff': cutoff,
                               'n': nmax,
                               'l': lmax,
                               'atom_gaussian_width': atom_gaussian_width}}
    for k in soap_spec.keys():
        soap_spec[k]['rbf'] = rbf
        soap_spec[k]['crossover'] = crossover
    # The specification for the kernels
    kernel_spec = dict(set_kernel(kernel_type, element_wise, zeta))
    # The specification for the descriptor
    desc_spec = {}
    for k, v in soap_spec.items():
        desc_spec[k] = {'atomic_descriptor': dict({k: v}),
                        'kernel_function': kernel_spec}
    # specify descriptors using the cmd line tool
    ctx.obj['descriptors'][tag] = desc_spec
    # Compute the save the descriptors
    output_desc(ctx.obj['asapxyz'], ctx.obj['descriptors'], ctx.obj['desc_options']['prefix'], peratom)

@gen_desc.command('cm')
@click.pass_context
@desc_options
def cm(ctx, tag):
    """Generate the Coulomb Matrix descriptors"""
    # load up the xyz
    ctx.obj['asapxyz'] = ASAPXYZ(ctx.obj['data']['fxyz'], ctx.obj['data']['stride'], ctx.obj['data']['periodic'])
    # The specification for the descriptor
    ctx.obj['descriptors'][tag] = {'cm':{'type': "CM"}}
    # Compute the save the descriptors
    output_desc(ctx.obj['asapxyz'], ctx.obj['descriptors'], ctx.obj['desc_options']['prefix'])

@gen_desc.command('run')
@click.pass_context
def run(ctx):
    """ Running analysis using input files """
    # load up the xyz
    ctx.obj['asapxyz'] = ASAPXYZ(ctx.obj['data']['fxyz'], ctx.obj['data']['stride'], ctx.obj['data']['periodic'])
    # Compute the save the descriptors
    output_desc(ctx.obj['asapxyz'], ctx.obj['descriptors'], ctx.obj['desc_options']['prefix'])
