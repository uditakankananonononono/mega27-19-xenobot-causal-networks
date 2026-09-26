import numpy as np
from src.real_calcium_sensor_focal import features,fit,score

def test_disjoint_parity_and_no_future():
 a=np.arange(30*110,dtype=float).reshape(30,110)
 x,y=features(a,True,True)
 assert x.shape==(15*109,3) and y.shape==(15,109)
 np.testing.assert_array_equal(x[:109,1],a[1,:-1]);np.testing.assert_array_equal(x[:109,2],a[0::2,:-1].mean(axis=0))
 np.testing.assert_array_equal(y[0],a[1,1:])
 xx,yy=features(a,False,True)
 np.testing.assert_array_equal(xx[:109,1],a[0,:-1]);np.testing.assert_array_equal(yy[0],a[0,1:])

def test_models_share_targets():
 rng=np.random.default_rng(42);a=rng.normal(size=(30,110));train=[a,a*1.2]
 c0=fit(train,True,False);c1=fit(train,True,True)
 assert score(a,c0,True,False)['cells']==score(a,c1,True,True)['cells']==15
 np.testing.assert_array_equal(features(a,True,False)[1],features(a,True,True)[1])
