from django import forms


class PhLocationSelect(forms.Select):
    class Media:
        js = ('phlocation/js/phlocation.js',)

    template_name = 'phlocation/widgets/select.html'

    def __init__(self, *args, extra_classes='', **kwargs):
        kwargs['attrs'] = {'class': 'ph-location ' + extra_classes}
        super().__init__(*args, **kwargs)


class PhRegionSelect(PhLocationSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, extra_classes='region', **kwargs)


class PhDistrictProvinceSelect(PhLocationSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, extra_classes='district-province', **kwargs)


class PhCityMunicipalitySelect(PhLocationSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, extra_classes='city-municipality', **kwargs)


class PhBarangaySelect(PhLocationSelect):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, extra_classes='barangay', **kwargs)
