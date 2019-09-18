import unittest

import numpy

import chainer
import chainer.functions as F
from chainer import testing


@testing.parameterize(*testing.product({
    'dtype': [numpy.float16, numpy.float32, numpy.float64],
    'shape': [(5, 10)]
}))
@testing.inject_backend_tests(
    None,
    # CPU tests
    [
        {},
    ]
    # GPU tests
    + testing.product({
        'use_cuda': [True],
        'cuda_device': [0, 1],
    })
    # ChainerX tests
    + testing.product({
        'use_chainerx': [True],
        'chainerx_device': ['native:0', 'cuda:0', 'cuda:1']
    })
)
@testing.with_requires('scipy')
class TestZeta(testing.FunctionTestCase):

    def setUp(self):
        self.check_forward_options = {'atol': 1e-3, 'rtol': 1e-3}
        self.check_backward_options = {'atol': 1e-3, 'rtol': 1e-3}
        self.check_double_backward_options = {'atol': 1e-3, 'rtol': 1e-3}

        self._x = numpy.random.uniform(self.shape)

    def generate_inputs(self):
        q = numpy.random.uniform(self.shape)
        return q,

    def forward_expected(self, inputs):
        q, = inputs
        import scipy
        y_expect = scipy.special.zeta(self._x, q)
        return numpy.array(y_expect),

    def forward(self, inputs, device):
        q, = inputs
        y = F.zeta(device.send(self._x), q)
        return y,


@testing.parameterize(*testing.product({
    'dtype': [numpy.float16, numpy.float32, numpy.float64],
    'shape': [(5, 10)]
}))
@testing.without_requires('scipy')
class TestZetaExceptions(unittest.TestCase):
    def setUp(self):
        self.q = numpy.random.uniform(self.shape)
        self.func = F.zeta

    def check_forward(self, q_data):
        q = chainer.Variable(q_data)
        with self.assertRaises(ImportError):
            self.func(q, self._x)

    def test_zeta_forward_cpu(self):
        self.check_forward(self.q)


testing.run_module(__name__, __file__)
