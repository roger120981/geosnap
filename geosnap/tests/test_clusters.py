from geosnap import Community
import numpy as np
from geosnap import DataStore

reno = Community.from_census(msa_fips="39900",datastore=DataStore())
columns = ["median_household_income", "p_poverty_rate", "p_unemployment_rate",]

# Aspatial Clusters


def test_gm():

    r = reno.cluster(columns=columns, method="gaussian_mixture", best_model=True)
    assert len(r.gdf.gaussian_mixture.unique()) >= 5


def test_ward():
    r = reno.cluster(columns=columns, method="ward")
    assert len(r.gdf.ward.unique()) == 7


def test_spectral():

    r = reno.cluster(columns=columns, method="spectral")
    assert len(r.gdf.spectral.unique()) == 7


def test_kmeans():

    r = reno.cluster(columns=columns, method="kmeans")
    assert len(r.gdf.kmeans.unique()) == 7


def test_aff_prop():

    r = reno.cluster(columns=columns, method="affinity_propagation", cluster_kwargs=dict(preference=-100))
    assert len(r.gdf.affinity_propagation.unique()) == 3


def test_hdbscan():

    r = reno.cluster(columns=columns, method="hdbscan")
    assert len(r.gdf.hdbscan.unique()) >= 4


# Spatial Clusters


def test_spenc():

    r = reno.regionalize(columns=columns, method="spenc")
    assert len(r.gdf.spenc.unique()) >= 6


def test_maxp_count():

    r = reno.regionalize(columns=columns, method="max_p", region_kwargs=dict(initial=10))
    assert len(r.gdf.max_p.unique()) >= 8

def test_maxp_thresh():

    r = reno.regionalize(columns=columns, method="max_p", region_kwargs=dict(initial=10), threshold_variable='n_total_pop', threshold=10000)
    assert len(r.gdf.max_p.unique()) >= 8


def test_ward_spatial():

    r = reno.regionalize(columns=columns, method="ward_spatial", n_clusters=7)
    assert len(r.gdf.ward_spatial.unique()) == 8


def test_skater():

    r = reno.regionalize(columns=columns, method="skater", n_clusters=10)
    assert len(r.gdf.skater.unique()) == 11


def test_azp():
    r = reno.regionalize(columns=columns, method="azp", n_clusters=7)
    assert len(r.gdf.azp.unique()) == 8


# Test seeding

def test_seed():
    np.random.seed(12345)
    r = reno.cluster(columns=columns, method='ward')
    card = r.gdf.groupby('ward').count()['geoid'].values
    np.testing.assert_array_equal(card, [27, 83, 19, 51, 38, 7])
