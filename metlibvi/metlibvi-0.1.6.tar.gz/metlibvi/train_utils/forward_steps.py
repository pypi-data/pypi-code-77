import torch

from metlibvi.train_utils.losses import metropolized_loss, kl_loss


def vanilla_vi_forward(transitions, target_logprob, prior, z, x=None, loss_variant='standard'):
    """
    The function implements forward step for vanilla variational inference
    :param loss_variant: specific version of the loss function
    :param transitions: transitions, represented ad a Modulelist
    :param target_logprob: a function, which computes target's logprob
    :param prior: a prior distribution for samples (std normal or induced by encoder)
    :param z: a batch of initial (not yet transformed) samples (e.g. from standard normal)
    :param x: a batch of data objects (if any)
    :return: returns mean KL divergence
    """

    final_samples, sum_log_jac = transitions(z.clone())

    kl = kl_loss(final_samples=final_samples, z=z, x=x, prior=prior, sum_log_jac=sum_log_jac,
                 target_logprob=target_logprob, loss_variant=loss_variant)

    return kl


def metropolized_vi_forward(transitions, target_logprob, prior, z, x=None, loss_variant='standard'):
    """
    The function returns forward step for metropolized vi
    :param transitions: transitions, represented ad a Modulelist
    :param target_logprob: a function, which computes target's logprob
    :param prior: a prior distribution for samples (std normal or induced by encoder)
    :param z: a batch of initial (not yet transformed) samples (e.g. from standard normal)
    :param x: a batch of data objects (if any)
    :param loss_variant: specific version of the loss function
    :return: returns loss (precomputed grad) for metropolized algorithms
    """
    sum_log_alphas = torch.zeros_like(z[:, 0])
    sum_log_jac = torch.zeros_like(z[:, 0])
    sum_log_probs = torch.zeros_like(z[:, 0])

    z_cur = z.clone()

    for i in range(len(transitions)):
        output = transitions[i](z=z_cur, target_logprob=target_logprob, x=x)

        sum_log_alphas = sum_log_alphas + output['current_log_alphas']
        sum_log_jac = sum_log_jac + output.get('log_jac', sum_log_jac)
        sum_log_probs = sum_log_probs + output.get('log_prob', sum_log_probs)
        z_cur = output['z_new']

    loss = metropolized_loss(final_samples=z_cur, z=z, x=x, prior=prior, sum_log_jac=sum_log_jac,
                             sum_log_alphas=sum_log_alphas, sum_log_probs=sum_log_probs, target_logprob=target_logprob,
                             loss_variant=loss_variant)

    return loss
