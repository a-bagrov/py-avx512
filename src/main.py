from mask import Mask
from zmm import ZMM
from operation import Operation
from block import Block
from cfg import CFG

# --------------------------------------------------------------------------------------------------


def sample_guessp_cfg():
    """
    CFG for guessp function of riemann solver.
    :return: CFG
    """

    # Constants.
    gama = 1.4
    g1 = (gama - 1.0) / (2.0 * gama)
    g2 = (gama + 1.0) / (2.0 * gama)
    g3 = (2.0 * gama) / (gama - 1.0)
    g4 = 2.0 / (gama - 1.0)
    g5 = 2.0 / (gama + 1.0)
    g6 = (gama - 1.0) / (gama + 1.0)
    g7 = (gama - 1.0) / 2.0
    g8 = gama - 1.0

    cfg = CFG()

    # Input parameters.
    dl = cfg.alloc_zmm('f')
    ul = cfg.alloc_zmm('f')
    pl = cfg.alloc_zmm('f')
    cl = cfg.alloc_zmm('f')
    dr = cfg.alloc_zmm('f')
    ur = cfg.alloc_zmm('f')
    pr = cfg.alloc_zmm('f')
    cr = cfg.alloc_zmm('f')

    # Output parameters.
    pm = cfg.alloc_zmm('f')

    # Blocks.
    b0 = cfg.alloc_block()
    b1 = cfg.alloc_block()
    b2 = cfg.alloc_block()
    b3 = cfg.alloc_block()
    b4 = cfg.alloc_block()
    b5 = cfg.alloc_block()

    # b0
    quser = b0.op('set-f', [2.0])
    cup = b0.op('mul-f',
                [b0.op('mul-f',
                       [b0.op('set-f', [0.25]),
                        b0.op('add-f', [dl, dr])]),
                 b0.op('add-f', [cl, cr])])
    ppv1 = b0.op('add-f',
                 [b0.op('mul-f',
                        [b0.op('set-f', [0.5]),
                         b0.op('add-f', [pl, pr])]),
                  b0.op('mul-f',
                        [b0.op('mul-f',
                               [b0.op('set-f', [0.5]),
                                b0.op('sub-f', [ul, ur])]),
                         cup])])
    ppv = b0.op('blend-f',
                [ppv1,
                 b0.op('set-f', [0.0])],
                b0.op('cmpgt-f',
                      [ppv1,
                       b0.op('set-f', [0.0])]))
    pmin = b0.op('blend-f', [pl, pr], b0.op('cmplt-f', [pl, pr]))
    pmax = b0.op('blend-f', [pl, pr], b0.op('cmpgt-f', [pl, pr]))
    qmax = b0.op('div-f', [pmax, pmin])
    b1_pred = b0.op('and-m',
                    [b0.op('and-m',
                           [b0.op('cmple-f', [qmax, quser]),
                            b0.op('cmple-f', [pmin, ppv])]),
                     b0.op('cmple-f', [ppv, pmax])])
    b0.jump(b1_pred, True, b1)
    b0.jump(b1_pred, False, b2)

    # b1
    b1.add_operation(Operation('mov-f', [ppv], pm))
    b1.jump(None, None, b5)

    # b2
    b3_pred = b2.op('cmplt-f', [ppv, pmin])
    b2.jump(b3_pred, True, b3)
    b2.jump(b3_pred, False, b4)

    # b3
    pq = b3.op('pow-f',
               [b3.op('div-f', [pl, pr]),
                b3.op('set-f', [g1])])
    um = b3.op('div-f',
               [b3.op('add-f',
                      [b3.op('add-f',
                             [b3.op('mul-f',
                                    [pq,
                                     b3.op('div-f', [ul, cl])]),
                              b3.op('div-f', [ur, cr])]),
                       b3.op('mul-f',
                             [b3.op('set-f', [g4]),
                              b3.op('sub-f',
                                    [pq,
                                     b3.op('set-f', [1.0])])])]),
                b3.op('add-f',
                      [b3.op('div-f', [pq, cl]),
                       b3.op('div-f',
                             [b3.op('set-f', [1.0]),
                              cr])])])
    ptl = b3.op('add-f',
                [b3.op('set-f', [1.0]),
                 b3.op('mul-f',
                       [b3.op('set-f', [g7]),
                        b3.op('div-f',
                              [b3.op('sub-f', [ul, um]),
                               cl])])])
    ptr = b3.op('add-f',
                [b3.op('set-f', [1.0]),
                 b3.op('mul-f',
                       [b3.op('set-f', [g7]),
                        b3.op('div-f',
                              [b3.op('sub-f', [um, ur]),
                               cr])])])
    pm_b3 = b3.op('mul-f',
                  [b3.op('set-f', [0.5]),
                   b3.op('add-f',
                         [b3.op('pow-f',
                                [b3.op('mul-f', [pl, ptl]),
                                 b3.op('set-f', [g3])]),
                          b3.op('pow-f',
                                [b3.op('mul-f', [pr, ptr]),
                                 b3.op('set-f', [g3])])])])
    b3.add_operation(Operation('mov-f', [pm_b3], pm))
    b3.jump(None, None, b5)

    # b4
    gel = b4.op('sqrt-f',
                [b4.op('div-f',
                       [b4.op('div-f',
                              [b4.op('set-f', [g5]),
                               dl]),
                        b4.op('add-f',
                              [b4.op('mul-f',
                                     [b4.op('set-f', [g6]),
                                      pl]),
                               ppv])])])
    ger = b4.op('sqrt-f',
                [b4.op('div-f',
                       [b4.op('div-f',
                              [b4.op('set-f', [g5]),
                               dr]),
                        b4.op('add-f',
                              [b4.op('mul-f',
                                     [b4.op('set-f', [g6]),
                                      pr]),
                               ppv])])])
    pm_b4 = b4.op('div-f',
                  [b4.op('sub-f',
                         [b4.op('add-f',
                                [b4.op('mul-f', [gel, pl]),
                                 b4.op('mul-f', [ger, pr])]),
                          b4.op('sub-f', [ur, ul])]),
                   b4.op('add-f', [gel, ger])])
    b4.add_operation(Operation('mov-f', [pm_b4], pm))
    b4.jump(None, None, b5)

    return cfg


# ==================================================================================================

if __name__ == '__main__':

    cfg = sample_guessp_cfg()
    for i in range(8):
        cfg.ZMMs[i].set_all_elements(1.0)

    # Emulate.
    # cfg.emulate_all()

    # Print.
    cfg.print_s()
    # cfg.print_l()

# ==================================================================================================
