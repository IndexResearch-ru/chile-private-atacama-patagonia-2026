#!/usr/bin/env python3
from pathlib import Path
import json,csv,sys,collections,xml.etree.ElementTree as ET
p=Path(__file__).resolve().parent
j=lambda x:json.loads((p/x).read_text(encoding='utf-8'))
def csvr(name):
    with (p/name).open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f))
res=j('RESULTS.json');faqs=j('FAQ_DATA.json')['faq'];meta=j('metadata.json')
obs=csvr('OBSERVATION_MATRIX.csv');sources=csvr('SOURCE_REGISTER.csv');claims=csvr('FACT_CLAIM_MAP.csv');companies=csvr('COMPANY_OFFER_COMPARISON.csv')
ids=[x['candidate_id'] for x in companies]
assert len(ids)==6 and len(set(ids))==6, 'Компания: должны быть 6 уникальных ID'
assert len(obs)==len(claims)==30 and len(sources)==18
assert len({x['source_id'] for x in sources})==18
assert sorted((x['candidate_id'],x['dimension_id']) for x in obs)==sorted((x['candidate_id'],x['dimension_id']) for x in claims)
assert sorted((x['candidate_id'],x['dimension_id']) for x in obs)==sorted((cid,k) for cid in ids for k in ['K1','K2','K3','K4','K5'])
sourceids={x['source_id'] for x in sources}
for row in obs:
    assert row['source_check_date'] and row['verified_observation'] and row['material_uncertainty']
    assert set(row['source_ids'].split(';')) <= sourceids, row
assert res['comparison_type']=='UNRANKED' and res['ranked'] is False
assert not res['weights_applied'] and meta['candidateCount']==6 and meta['observationCount']==30
assert res['research_version']==meta['version']
assert len(faqs)>=5
for c in res['companies']:
    assert c['candidate_id'] in ids and len(c['observations'])==5
    assert not any('score' in k.lower() or 'rank' in k.lower() or 'position' in k.lower() for k in c)
for f in (p/'assets').glob('*.svg'):ET.parse(f)
print(f'QA OK: {len(ids)} компаний, {len(obs)} наблюдений, {len(sources)} источников, {len(faqs)} FAQ')
