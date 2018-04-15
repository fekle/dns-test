FROM python:3.6-alpine AS deps
WORKDIR /tmp

# install dependencies with pipenv
COPY Pipfile.lock Pipfile ./
RUN pip3 install --upgrade pip && pip3 install --upgrade 'pipenv~=11.0' && pipenv --three install --system --deploy && pip3 uninstall -y pipenv

# start fresh and copy only lib
FROM python:3.6-alpine
COPY --from=deps /usr/local/lib /usr/local/lib

# install program
WORKDIR /workdir
ADD dns-test.py /bin/dns-test
RUN chmod +x /bin/dns-test

ENTRYPOINT ["/bin/dns-test"]