FROM python:3.6-alpine AS deps

RUN pip --no-cache-dir install 'pipenv~=11.0'

WORKDIR /workdir
COPY Pipfile.lock Pipfile ./
RUN pipenv --site-packages --three install --system --deploy && pip --no-cache-dir uninstall -y pipenv

FROM python:3.6-alpine
COPY --from=deps /usr/local/lib/python3.6 /usr/local/lib/python3.6

ADD dnsavg.py /bin/dnsavg
RUN chmod +x /bin/dnsavg

ENTRYPOINT ["/bin/dnsavg"]