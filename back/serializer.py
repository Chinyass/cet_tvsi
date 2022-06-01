from .models import ATS,OLT

def get_ats():
    ats_query = ATS.objects.all()
    res = []
    for ats in ats_query:
        olts_query = ats.olt.all()
        olts = []
        for olt in olts_query:
            olts.append({
                'ip':olt.ip,
                'model':olt.model,
                'firmware':olt.firmware
            })

        res.append({
            'name':ats.name,
            'location':ats.location,
            'olts': olts
        })

    return res