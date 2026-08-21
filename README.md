## Edu Tz

edu_tz

#### License

MIT

#### NMB fee integration

The NMB Bank fee integration (callback token, invoice submission, payment
callbacks, reconciliation) lives in `edu_tz.edu_tz.nmb.api`. New invoices send
`/api/method/edu_tz.edu_tz.nmb.api.receive_callback` as their callback URL.
Invoices submitted before the move from `csf_tz` still call
`csf_tz.bank_api.receive_callback`, which forwards to this app.
