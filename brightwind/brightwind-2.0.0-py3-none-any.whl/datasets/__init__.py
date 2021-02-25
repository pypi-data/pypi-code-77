
import os

__all__ = ['demo_data', 'demo_campbell_scientific_data', 'demo_campbell_scientific_site_data', 'demo_merra2_NW',
           'demo_merra2_NE', 'demo_merra2_SE', 'demo_merra2_SW', 'demo_windographer_data',
           'shell_flats_80m_csv', 'shell_flats_50m_csv', 'shell_flats_merra', 'demo_windographer_site_data']

shell_flats_80m_csv = os.path.join(os.path.dirname(__file__), 'offshore-CREYAP-2-data-pack', 'Shell_Flats_1_80mHAT.csv')
shell_flats_50m_csv = os.path.join(os.path.dirname(__file__), 'offshore-CREYAP-2-data-pack', 'Shell_Flats_2_50mHAT.csv')
shell_flats_merra = os.path.join(os.path.dirname(__file__), 'offshore-CREYAP-2-data-pack', 'MERRA_W03.332_N54.000.csv')

demo_campbell_scientific_data = os.path.join(os.path.dirname(__file__), 'demo', 'campbell_scientific_demo_data.csv')
demo_data = os.path.join(os.path.dirname(__file__), 'demo', 'demo_data.csv')
demo_windographer_data = os.path.join(os.path.dirname(__file__), 'demo', 'windographer_demo_data.txt')
# -------- depreciate ----------
demo_campbell_scientific_site_data = os.path.join(os.path.dirname(__file__), 'demo',
                                                  'campbell_scientific_demo_site_data_clean.csv')
demo_windographer_site_data = os.path.join(os.path.dirname(__file__), 'demo', 'windographer_demo_site_data.txt')
# -------- depreciate ----------

demo_merra2_NW = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_NW_2000-01-01_2017-06-30.csv')
demo_merra2_NE = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_NE_2000-01-01_2017-06-30.csv')
demo_merra2_SE = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_SE_2000-01-01_2017-06-30.csv')
demo_merra2_SW = os.path.join(os.path.dirname(__file__), 'demo', 'MERRA-2_SW_2000-01-01_2017-06-30.csv')


def datasets_available():
    """
    Example datasets that can be used with the library.


    **Example usage**
    ::
        import brightwind as bw

        all_datasets_available = ['demo_campbell_scientific_site_data', 'demo_merra2_NW', 'demo_merra2_NE',
            'demo_merra2_SE', 'demo_merra2_SW', 'shell_flats_80m_csv', 'shell_flats_50m_csv', 'shell_flats_merra']
        shell_flats_80m_csv = bw.load_csv(bw.datasets.shell_flats_80m_csv)
        shell_flats_50m_csv = bw.load_csv(bw.datasets.shell_flats_50m_csv)
        shell_flats_merra = bw.load_csv(bw.datasets.shell_flats_merra)
        demo_data = bw.load_campbell_scientific(bw.datasets.demo_campbell_scientific_site_data)
        demo_data = bw.load_csv(bw.datasets.demo_data)
        demo_windog_data = bw.load_windographer_txt(bw.datasets.demo_windographer_site_data)

    """

    return None
