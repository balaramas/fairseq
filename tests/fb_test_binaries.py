# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import contextlib
from io import StringIO
import tempfile
import unittest

import torch

from tests.test_binaries import (
    create_dummy_data,
    preprocess_translation_data,
    train_translation_model,
    generate_main,
)


class TestTranslation(unittest.TestCase):

    @unittest.skipIf(not torch.cuda.is_available(), 'test requires a GPU')
    def test_fb_levenshtein_transformer(self):
        with contextlib.redirect_stdout(StringIO()):
            with tempfile.TemporaryDirectory('test_fb_levenshtein_transformer') as data_dir:
                create_dummy_data(data_dir)
                preprocess_translation_data(data_dir, ['--joined-dictionary'])
                train_translation_model(data_dir, 'fb_levenshtein_transformer', [
                    '--apply-bert-init', '--early-exit', '6,6,6',
                    '--criterion', 'nat_loss'
                ], task='translation_lev')
                generate_main(data_dir, [
                    '--task', 'translation_lev',
                    '--iter-decode-max-iter', '9',
                    '--iter-decode-eos-penalty', '0',
                    '--print-step',
                ])


if __name__ == '__main__':
    unittest.main()