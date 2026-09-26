"""Judge-11 post-outcome synthetic proxy stress test, not causal biology."""
import json
import numpy as np
from src.synthetic_calibration import SCENARIOS,generate
from src.observed_driver_sensitivity import generate_with_driver,features,fit,score

LEVELS=(None,0.0,0.5,2.0)

def sample(seed,g,h,idx,proxy_index):
    a,u=generate_with_driver(seed,g,h)
    np.testing.assert_array_equal(a,generate(seed,g,h))
    if proxy_index==0:return a,np.zeros_like(u)
    sigma=LEVELS[proxy_index]
    rng=np.random.default_rng(3000000+idx*10000+(seed-20260926-idx*10000)+100000*proxy_index)
    p=u+sigma*rng.normal(size=u.shape)
    return a,p

def run(seed=20260926):
    result={'status':'POST-OUTCOME JUDGE-11 IMPERFECT-PROXY SYNTHETIC DIAGNOSTIC, NOT BIOLOGY OR BENCHMARK BEAT',
            'protocol':'docs/JUDGE_11_PROXY_BENCH_PROTOCOL.md','seed':seed,'scenarios':{}}
    for idx,(name,(g,h)) in enumerate(SCENARIOS.items()):
        case={}
        for proxy_index,level in enumerate(LEVELS):
            series=[sample(seed+idx*10000+i,g,h,idx,proxy_index) for i in range(24)]
            if proxy_index==0:
                # No-proxy means exclude the covariate, not include a zero column.
                from src.organoid_method import train as plain_fit,score as plain_score
                own=plain_fit([x[0] for x in series[:16]],False)
                pop=plain_fit([x[0] for x in series[:16]],True)
                def evaluate(a,p):return plain_score(a,own,False),plain_score(a,pop,True)
            else:
                own=fit(series[:16],False);pop=fit(series[:16],True)
                def evaluate(a,p):return score(a,p,own,False),score(a,p,pop,True)
            rows=[]
            for i in range(16,24):
                s,b=evaluate(*series[i]);rows.append({'replicate':i,'nested_baseline_rmse':s,'population_rmse':b,'relative_gain':(s-b)/s})
            case['none' if level is None else str(level)]={'proxy_noise_sd':level,'model_a_coef':own.tolist(),
                         'model_b_coef':pop.tolist(), 'heldout':rows,
                         'mean_relative_gain':float(np.mean([x['relative_gain'] for x in rows]))}
        result['scenarios'][name]={'g':g,'h':h,'proxy_levels':case}
    return result
if __name__=='__main__':print(json.dumps(run(),indent=2))
