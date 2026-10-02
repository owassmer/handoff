# pipeline/data snapshot

Snapshot taken 2026-09-30T21:35:23+00:00 (UTC) from /Users/owenwassmer/.hermes/profiles/ferro/cache/scratch/pipeline_import_test/register. Files read (copies), with sha256 and last-modified time:

- `register/calibration_negatives.json` 07d79aac5f622dff46e48266d5149df20b2665fc222940f9a2ecf1b2d6441a45 (modified 2026-09-30T07:42:39+00:00)
- `register/instruments.json` f893db3c58c29a45ff59f7ead22e09da11cb7118becc65e178b110e8fffd6312 (modified 2026-09-30T17:37:09+00:00)
- `register/sections.jsonl` 5fc7624a839d7070fa417ed8db1b5ff6bc471d91dc3b05b2e143321bb169065a (modified 2026-09-30T17:37:09+00:00)
- `register/triage.jsonl` 1acf4a18f8d5cad1274fc8ddeda4e79d164ad490f7483359f236213c4d30d490 (modified 2026-09-30T17:37:09+00:00)
- `register/work/batch_1.json` dcd8475f7c7f61df3b681a95d61541351e2d3c4fe217a5db54d43f2dd3a1433b (modified 2026-09-30T15:55:11+00:00)
- `register/work/batch_2.json` 2434befc0166c22bf52d010a415342904135459ff1aa55a8ec13dce775312b4c (modified 2026-09-30T15:55:11+00:00)
- `register/work/batch_3.json` 03f76eb7c7bf86628dba7aec65189bee7fa96aef37f38d898ea846a0dc4ecf6f (modified 2026-09-30T15:55:11+00:00)
- `register/work/batch_4.json` e4598bb19d27eff111f02022570465c31358b45adae168d453e72c525278fcf0 (modified 2026-09-30T15:55:11+00:00)
- `register/work/batch_5.json` 4e1805ecde620e3eed93b71108631cb1e05284191e291d126906f2c4894e71fa (modified 2026-09-30T15:55:11+00:00)
- `register/work/batch_6.json` 7f614107d0382c2437a0e092b61b0cad24ccff3b629c76e08c61f4ebd77103b1 (modified 2026-09-30T15:55:11+00:00)
- `register/work/batch_7.json` 49813ba8617c2cac5943e61d8b25824d8f6e75e42d1d0d4227ff19ca96eda082 (modified 2026-09-30T16:36:35+00:00)
- `register/work/batch_8.json` 1c96f98c91d9cd557a52b6f4293e0583fcf65c03e502cbc0f563e6396b2d1a30 (modified 2026-09-30T16:36:35+00:00)
- `register/work/batch_9.json` 7addfcfcb176d35c85f914cad380633fef04e83c084eb8cbbf4d4a416c3b4553 (modified 2026-09-30T17:37:09+00:00)
- `register/work/decisions_1.jsonl` ee2ddd35375796953cda365e1c46d9fc43613c91a2f6a55b899a83610b2bffd4 (modified 2026-09-30T16:33:27+00:00)
- `register/work/decisions_2.jsonl` 192bf9e6054533681add35a22599f9a24e1c8bc0c0e0f8109cfb7241b3f5c548 (modified 2026-09-30T16:30:47+00:00)
- `register/work/decisions_3.jsonl` f478668ddc59f751e73fc94b03f136e17d52fd7f42ab9854829086dfe485e8ab (modified 2026-09-30T16:15:21+00:00)
- `register/work/decisions_4.jsonl` 6b5eb4b60bf9a110ec63ca78a6c3c70befdb0d4c9c4531f14bcf579ee41e3519 (modified 2026-09-30T16:23:06+00:00)
- `register/work/decisions_5.jsonl` 14e91856d76ea70686b37ed7c87e07db2009fcdd286427bf27fb4dee6b0e6b42 (modified 2026-09-30T16:27:40+00:00)
- `register/work/decisions_6.jsonl` e8e26d9780519108cb12b044f2b12767792158a4a5988542827010b75a087de6 (modified 2026-09-30T16:24:11+00:00)
- `register/work/decisions_7.jsonl` 615e001a052b5de2181f6e87cd0085ccf98cada04583aaa821d9a5059119c4a5 (modified 2026-09-30T16:50:09+00:00)
- `register/work/decisions_8.jsonl` 6d2755ec67ba067ecb5bf599943edb0363cb95f282a53e1c2c8421db134f9c49 (modified 2026-09-30T16:49:17+00:00)
- `register/work/decisions_9.jsonl` e5a9442a97b53011b931face935c04f26f32cf5b13be76456f8183079e9f935f (modified 2026-09-30T17:37:09+00:00)

Gold labels by jurisdiction and decision:

- NY excluded_regime: 60
- NY new_rule: 304
- NY no_decision: 1734
- NY partial: 100
- NY stated: 212
- NYC excluded_regime: 48
- NYC new_rule: 28
- NYC no_decision: 405
- NYC partial: 14
- NYC stated: 93
- US excluded_regime: 3
- US new_rule: 135
- US no_decision: 474
- US partial: 19
- US stated: 93

deciding = decision in stated, partial, new_rule. The decisions are the reviewers' (every batch in register/work) or, for sections a rule already cited, 'stated' by the register's match (decided_by 'match'). Jev scores are registry 1.0.0.
Calibration (`python3 -m pipeline calibrate CODE`) takes the deciding rows whose functions overlap the jurisdiction's instruments as gold positives; text_file is the imported path, legacy_text_file the register path (read when the jurisdiction folders are not imported).
