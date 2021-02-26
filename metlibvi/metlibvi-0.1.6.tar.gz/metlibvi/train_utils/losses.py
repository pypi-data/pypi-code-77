import torch


def metropolized_loss(final_samples, z, x, prior, sum_log_jac, sum_log_alphas, sum_log_probs, target_logprob,
                      loss_variant):
    if loss_variant == 'standard':
        elbo = target_logprob(z=final_samples, x=x) - (prior.log_prob(z).sum(-1) - sum_log_jac + sum_log_alphas)
        grad_elbo = elbo + elbo.detach() * (sum_log_alphas + sum_log_probs).mean()
        return -grad_elbo


def kl_loss(final_samples, z, x, prior, sum_log_jac, target_logprob, loss_variant):
    if loss_variant == 'standard':
        return torch.mean(prior.log_prob(z).sum(-1) - sum_log_jac - target_logprob(z=final_samples, x=x))
