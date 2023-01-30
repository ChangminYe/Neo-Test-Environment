import torch

##### Define approximate firing function #####
class ActFun(torch.autograd.Function):

    @staticmethod
    def forward(ctx, input, thresh):
        ctx.save_for_backward(input)
        return input.gt(thresh).float()

    @staticmethod
    def backward(ctx, grad_output, thresh):
        input, = ctx.saved_tensors
        grad_input = grad_output.clone()
        temp = abs(input - thresh) < lens
        return grad_input * temp.float()

act_fun = ActFun.apply
##############################################


########### SRM neuron model membrane potential update ###########
def mem_update(ops, x, mem1, mem2, spike, decay1, decay2, const, thresh):
    mem1 = mem1 * decay1 * (1. - spike) + const * ops(x)
    mem2 = mem2 * decay2 * (1. - spike) + const * ops(x)
    mem = mem1 - mem2
    spike = act_fun(mem, thresh) # act_fun : approximation firing function
    return mem1, mem2, spike
##################################################################