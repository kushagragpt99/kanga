import numpy as np

from pathlib import Path

import kanga.stats as st

class ChainArray:
    def __init__(self, vals):
        self.reset(vals)

    def reset(self, vals):
        self.vals = vals

    @classmethod
    def from_file(selfclass, keys=['sample', 'target_val', 'accepted'], path=Path.cwd(), dtype=np.float64):
        vals = {}

        for key in keys:
            vals[key] = np.loadtxt(Path(path).joinpath(key+'.csv'), dtype=int if key == 'accepted' else dtype, delimiter=',')

        return selfclass(vals)

    def __repr__(self):
        return f"Markov chain containing {len(self.vals['sample'])} samples."

    def __len__(self):
        return self.num_samples()

    def num_params(self):
        return len(self.get_sample(0))

    def num_samples(self):
        return len(self.get_samples())

    def get_param(self, idx):
        return self.vals['sample'][:, idx]

    def get_sample(self, idx):
        return self.vals['sample'][idx, :]

    def get_samples(self):
        return self.vals['sample']

    def get_target_vals(self):
        return self.vals['target_val']

    def get_grad_val(self, idx):
        return self.vals['grad_val'][idx, :]

    def get_grad_vals(self):
        return self.vals['grad_val']

    def state(self, idx=-1):
        current = {}
        for key, val in self.vals.items():
            try:
                current[key] = val[idx]
            except IndexError:
                print(f'WARNING: chain does not have values for {key}.')
                pass
        return current

    def mean(self):
        return self.get_samples().mean(0)

    def running_mean(self, idx):
        return np.array(st.running_mean(self.get_param(idx)))

    def running_means(self):
        return np.transpose(np.array([self.running_mean(i) for i in range(self.num_params())]))

    def mc_se(self, mc_cov_mat=None, method='inse', adjust=False, b=None, r=3):
        if mc_cov_mat is None:
            return st.mc_se(self.get_samples(), method=method, adjust=adjust, b=b, r=r, rowvar=False)
        else:
            return st.mc_se_from_cov(mc_cov_mat)

    def mc_cov(self, method='inse', adjust=False, b=None, r=3):
        return st.mc_cov(self.get_samples(), method=method, adjust=adjust, b=b, r=r, rowvar=False)

    def mc_cor(self, mc_cov_mat=None, method='inse', adjust=False, b=None, r=3):
        if mc_cov_mat is None:
            return st.mc_cor(self.get_samples(), method=method, adjust=adjust, b=b, r=r, rowvar=False)
        else:
            return st.cor_from_cov(mc_cov_mat)

    def acceptance_rate(self):
        return sum(self.vals['accepted']) / self.num_samples()

    def block_acceptance_rate(self):
        return np.array(self.vals['accepted']).sum(axis=0) / self.num_samples()

    def multi_ess(self, mc_cov_mat=None, method='inse', adjust=False, b=None, r=3):
        return st.multi_ess(self.get_samples(), mc_cov_mat=mc_cov_mat, method=method, adjust=adjust, b=b, r=r)

    def savecsv(self, keys=None, path=Path.cwd(), fmt=None):
        keys = keys or self.vals.keys()
        fmt = fmt or ['%.18e' for _ in range(len(keys))]

        for i, key in enumerate(keys):
            np.savetxt(path.joinpath(key+'.csv'), self.vals[key], fmt=fmt[i], delimiter=',')
