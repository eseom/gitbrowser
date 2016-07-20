from datetime import datetime

dataset = [
    dict(
        model='flamengo.models.Repo',
        records=[
            dict(
                group='samplegroup',
                name='samplename',
                created_at=datetime.now(),
                updated_at=datetime.now(),
                type='public',
                description='sample description',
            )
        ]
    )
]
