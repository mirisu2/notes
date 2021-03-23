https://github.com/acmesh-official/acme.sh/wiki/DNS-alias-mode  
+  
https://github.com/acmesh-official/acme.sh/wiki/DNS-manual-mode  

#### 1. [Install](https://github.com/acmesh-official/acme.sh/wiki/How-to-install) acme.sh:
```
curl https://get.acme.sh | sh -s email=my@example.com
or
wget -O -  https://get.acme.sh | sh -s email=my@example.com
```

#### 2. Задаем на каждом dns сервере для которого надо запросить сертификат 
```
sudo vi /etc/named/zones/db.myzone.gg

_acme-challenge         IN      CNAME   _acme-challenge.YOUR.DOMAIN.RU.
```

#### 3. Запрашиваем сертификат
```
$ acme.sh --issue -d OKD.MYDOMAIN.RU [-d OSE.MYDOMAIN.COM] --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please --challenge-alias YOUR.DOMAIN.RU
[Tue Mar 23 20:57:46 MSK 2021] Using CA: https://acme-v02.api.letsencrypt.org/directory
[Tue Mar 23 20:57:47 MSK 2021] Create account key ok.
[Tue Mar 23 20:57:47 MSK 2021] Registering account: https://acme-v02.api.letsencrypt.org/directory
[Tue Mar 23 20:57:48 MSK 2021] Registered
[Tue Mar 23 20:57:49 MSK 2021] ACCOUNT_THUMBPRINT='ADwgoBvzNZmnOKKAheJUfnG0wxBfyRaUeEPFIAdomOQ'
[Tue Mar 23 20:57:49 MSK 2021] Creating domain key
[Tue Mar 23 20:57:49 MSK 2021] The domain key is here: /root/.acme.sh/OKD.MYDOMAIN.RU/OKD.MYDOMAIN.RU.key
[Tue Mar 23 20:57:49 MSK 2021] Single domain='OKD.MYDOMAIN.RU'
[Tue Mar 23 20:57:49 MSK 2021] Getting domain auth token for each domain
[Tue Mar 23 20:57:51 MSK 2021] Getting webroot for domain='OKD.MYDOMAIN.RU'
[Tue Mar 23 20:57:51 MSK 2021] Add the following TXT record:
[Tue Mar 23 20:57:51 MSK 2021] Domain: '_acme-challenge.YOUR.DOMAIN.RU'
[Tue Mar 23 20:57:51 MSK 2021] TXT value: 'WYB3J6MfMaNYIlp1Pr4jpVcujUY0YUEScj0Q'
[Tue Mar 23 20:57:51 MSK 2021] Please be aware that you prepend _acme-challenge. before your domain
[Tue Mar 23 20:57:51 MSK 2021] so the resulting subdomain will be: _acme-challenge.YOUR.DOMAIN.RU
[Tue Mar 23 20:57:51 MSK 2021] Please add the TXT records to the domains, and re-run with --renew.
[Tue Mar 23 20:57:51 MSK 2021] Please add '--debug' or '--log' to check more details.
[Tue Mar 23 20:57:51 MSK 2021] See: https://github.com/acmesh-official/acme.sh/wiki/How-to-debug-acme.sh
```

#### 4. Задаем на "центральном" dns сервере
```
_acme-challenge     IN   TXT   "WYB3J6MfMaNYIlp1Pr4jpVcujUY0YUEScj0Q"
```

#### 5. Подтверждаем 
```
$ acme.sh --renew -d OKD.MYDOMAIN.RU --dns --yes-I-know-dns-manual-mode-enough-go-ahead-please --challenge-alias YOUR.DOMAIN.RU --log [--debug]
[Tue Mar 23 21:06:42 MSK 2021] Renew: 'OKD.MYDOMAIN.RU'
[Tue Mar 23 21:06:43 MSK 2021] Using CA: https://acme-v02.api.letsencrypt.org/directory
[Tue Mar 23 21:06:43 MSK 2021] Single domain='OKD.MYDOMAIN.RU'
[Tue Mar 23 21:06:43 MSK 2021] Getting domain auth token for each domain
[Tue Mar 23 21:06:43 MSK 2021] Verifying: OKD.MYDOMAIN.RU
[Tue Mar 23 21:06:48 MSK 2021] Success
[Tue Mar 23 21:06:48 MSK 2021] Verify finished, start to sign.
[Tue Mar 23 21:06:48 MSK 2021] Lets finalize the order.
[Tue Mar 23 21:06:48 MSK 2021] Le_OrderFinalize='https://acme-v02.api.letsencrypt.org/acme/finalize/11634543579/8623454350'
[Tue Mar 23 21:06:49 MSK 2021] Downloading cert.
[Tue Mar 23 21:06:49 MSK 2021] Le_LinkCert='https://acme-v02.api.letsencrypt.org/acme/cert/04215a87a2e3e9bf843kj45kj43h5k435'
[Tue Mar 23 21:06:50 MSK 2021] Cert success.
-----BEGIN CERTIFICATE-----
MIIFGzCCBAOgAwIBA3r34r34rJ/oVRGBN0NLfMA0GCSq456456BCwUA
...
a1pYG65834r34runDXC
-----END CERTIFICATE-----
[Tue Mar 23 21:06:50 MSK 2021] Your cert is in  /root/.acme.sh/OKD.MYDOMAIN.RU/OKD.MYDOMAIN.RU.cer
[Tue Mar 23 21:06:50 MSK 2021] Your cert key is in  /root/.acme.sh/OKD.MYDOMAIN.RU/OKD.MYDOMAIN.RU.key
[Tue Mar 23 21:06:50 MSK 2021] The intermediate CA cert is in  /root/.acme.sh/OKD.MYDOMAIN.RU/ca.cer
[Tue Mar 23 21:06:50 MSK 2021] And the full chain certs is there:  /root/.acme.sh/OKD.MYDOMAIN.RU/fullchain.cer
```
