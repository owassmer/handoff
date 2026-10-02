from __future__ import print_function

import os
import platform
import ssl
import json
import base64
import collections

# Python 2/3 without using six
try:
    # Python 2
    from urllib2 import HTTPError, Request, urlopen
except ImportError:
    # Python3
    from urllib.error import HTTPError
    from urllib.request import Request, urlopen

### DO NOT MODIFY ###


def valid_file(f):
    supportedFileExts = (".md", ".png", ".jpg", ".jpeg", ".mp4", ".gif", ".rst", ".wav")
    root_dir = 'docs'

    return f['type'] == 'FILE' \
        and f['name'].endswith(supportedFileExts)\
        and f['path'].startswith(root_dir)


def build_ssl_ctx():
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    return ssl_ctx


def build_http_request(url, headers, method, data=None):
    if data is None:
        req = Request(url, headers=headers)
    else:
        data = json.dumps(data)
        # In Python 3 data is expected as bytes not as a string
        if is_python_3():
            data = data.encode('utf-8')
        req = Request(url, data=data, headers=headers)
        req = Request(url, data=data, headers=headers)
    req.get_method = lambda: method
    return req


def build_headers(token, content_type=None):
    headers = {'Authorization': 'Bearer {token}'.format(token=token)}
    if content_type is not None:
        headers['Content-type'] = content_type
    return headers


def perform_request(req, ssl_ctx):
    try:
        response = urlopen(req, context=ssl_ctx)
        return response
    except HTTPError as e:
        # Required for compatability with Python 2 and 3
        try:
            # Python 3
            response_bytes = e.read()
            enrich_foundry_exception(response_bytes)
            print(
                'Encountered HTTP error.\n',
                'HTTP Status code: {get_code}\n'.format(get_code=e.getcode()),
                'Reason: {reason}\n'.format(reason=e.reason),
                'Response: {response}'.format(response=response_bytes))
        except TypeError:
            # Python 2
            print(
                'Encountered HTTP error Python 2.\n',
                'HTTP Status code: {get_code}\n'.format(get_code=e.code),
                'Reason: {reason}\n'.format(reason=e.reason),
                'Response: {read}'.format(read=e.read()))
        raise e


def enrich_foundry_exception(response_bytes: bytes):
    try:
        error_json = json.loads(response_bytes.decode('utf-8'))
        error_name = error_json.get('errorName', 'Unknown')
        error_instance_id = error_json.get('errorInstanceId', 'missing error instance id')

        message = error_name
        if error_json.get('errorName') == 'Rosetta:FailedToPublishToAipAssistNoModelsAvailable':
            message = 'Failed to publish because no models were available. This may occur when AIP is not enabled for all organizations that this resource is marked with.'
        print(f'\nEncountered error ({error_instance_id}):\n{message}\n\n')
    except:
      pass

def put_request(url, data, token):
    headers = build_headers(token, 'application/json')
    ssl_ctx = build_ssl_ctx()
    req = build_http_request(url, headers, 'PUT', data)
    response = perform_request(req, ssl_ctx)
    return response


def get_request(url, token):
    headers = build_headers(token)
    ssl_ctx = build_ssl_ctx()
    req = build_http_request(url, headers, 'GET')
    response = perform_request(req, ssl_ctx)
    return response


def post_request(url, data, token):
    headers = build_headers(token, 'application/json')
    ssl_ctx = build_ssl_ctx()
    req = build_http_request(url, headers, 'POST', data)
    response = perform_request(req, ssl_ctx)
    return response


def decode(s):
    result = base64.b64decode(s)
    # Return type changed to bytes in Python 3
    if is_python_3():
        result = result.decode("utf-8")
    return result


def get_environment_variable(variable):
    if variable not in os.environ:
        raise RuntimeError('"%s" environment variable was not found.' % variable)
    if os.environ.get(variable) == 'https://ci-role-not-found':
        raise RuntimeError('"%s" role was not found.' % variable)
    return os.environ.get(variable)


def get_branch():
    return get_environment_variable('JEMMA_BRANCH')


def get_stemma_url():
    return get_environment_variable('STEMMA_API')


def get_rosetta_url():
    return get_environment_variable('ROSETTA_API')


def get_jemma_url():
    return get_environment_variable('JEMMA_API')


def get_repo_rid():
    return get_environment_variable('REPOSITORY_RID')


def get_token():
    return get_environment_variable('JOB_TOKEN')


def get_commitish():
    return get_environment_variable('STEMMA_REF')


def get_aip_assist_filename():
    return 'aip-assist.json'


def is_python_3():
    return platform.sys.version_info.major == 3


def get_file_metadata():
    commitish = get_commitish()
    repo_rid = get_repo_rid()
    token = get_token()
    file_paths = '{stemma_url}/repos/{repo_rid}/paths/contents/?recursive=true&commitish={commitish}'.format(stemma_url=get_stemma_url(),
                                                                                                             repo_rid=repo_rid,
                                                                                                             commitish=commitish)
    file_contents = json.load(get_request(file_paths, token))
    return [f for f in file_contents['directoryContents'] if valid_file(f)]


def get_security_mode():
    repo_rid = get_repo_rid()
    token = get_token()
    jemma_call = '{stemma_url}/security/{repo_rid}/mode'.format(stemma_url=get_jemma_url(),
                                                                repo_rid=repo_rid)
    return json.load(get_request(jemma_call, token))


def split_projects(files_metadata):
    projects = collections.defaultdict(list)
    for f in files_metadata:
        path = os.path.normpath(f['path'])
        split_path = path.split(os.sep)
        if len(split_path) >= 3:
            project = split_path[1]
            projects[project] += [f]
    return projects


def get_project_file_payload(files_metadata):
    payload_files = {}
    commitish = get_commitish()
    repo_rid = get_repo_rid()
    token = get_token()
    for f in files_metadata:
        request_url = '{stemma_url}/repos/{repo_rid}/paths/contents/{path}?recursive=false&commitish={commitish}'.format(stemma_url=get_stemma_url(),
                                                                                                                               repo_rid=repo_rid,
                                                                                                                               path=f['path'],
                                                                                                                               commitish=commitish)
        file_content_response = json.load(get_request(request_url, token))

        is_binary = file_content_response['metadata']['binary']

        content = file_content_response['fileContents'] if is_binary else decode(file_content_response['fileContents'])

        if is_binary:
            payload_file = {'media': content, 'type': 'media'}
        else:
            payload_file = {'markdown': content, 'type': 'markdown'}

        payload_files[f['path']] = payload_file

    return payload_files


def get_file_payload():
    files_metadata = get_file_metadata()
    project_file_metadata = split_projects(files_metadata)
    project_payloads = {proj: get_project_file_payload(files_metadata) for proj, files_metadata in project_file_metadata.items()}
    return project_payloads


def contains_aip_assist_file():
    commitish = get_commitish()
    repo_rid = get_repo_rid()
    token = get_token()
    root_dir_path = '{stemma_url}/repos/{repo_rid}/paths/contents/?recursive=true&commitish={commitish}'.format(stemma_url=get_stemma_url(),
                                                                                                                repo_rid=repo_rid,
                                                                                                                commitish=commitish)
    root_dir = json.load(get_request(root_dir_path, token))
    return any(f['name'] == get_aip_assist_filename() for f in root_dir['directoryContents'])



def get_aip_asist_file_payload():
    commitish = get_commitish()
    repo_rid = get_repo_rid()
    token = get_token()
    request_url = '{stemma_url}/repos/{repo_rid}/paths/contents/{path}?recursive=false&commitish={commitish}'.format(stemma_url=get_stemma_url(),
                                                                                                                     repo_rid=repo_rid,
                                                                                                                     path=get_aip_assist_filename(),
                                                                                                                     commitish=commitish)
    file_content_response = json.load(get_request(request_url, token))

    content = decode(file_content_response['fileContents'])

    payload_file = json.loads(content)

    return payload_file


def pretty_print_errors(errors):
    for error in errors:
        print('{error_level}: {message}'.format(error_level=error['errorLevel'],
                                                message=error['message']))
        args = error['args']
        for arg, value in args.items():
            print(format_arg(arg, value))
        print


def format_arg(arg, value):
    to_print = '\t{arg}: {value}'.format(arg=arg, value=value)
    max_chunk_len = 80
    to_print_chunks = [to_print[i:i+max_chunk_len] for i in range(0, len(to_print), max_chunk_len)]
    return '\n\t\t'.join(to_print_chunks)


def get_error_level_errors(errors):
    return list(filter(lambda error: (error['errorLevel'] == 'ERROR'), errors))


def get_allowed_words():
    commitish = get_commitish()
    repo_rid = get_repo_rid()
    token = get_token()
    request_url = '{stemma_url}/repos/{repo_rid}/paths/contents/allowed_words.txt?recursive=false&commitish={commitish}'.format(stemma_url=get_stemma_url(),
                                                                                                                                repo_rid=repo_rid,
                                                                                                                                commitish=commitish)
    try:
        allowed_words_file_contents = decode(json.load(get_request(request_url, token))['fileContents'])
        return list(filter(lambda word: len(word) > 0, allowed_words_file_contents.split("\n")))
    except:
        return []


def validate(allowed_words, docs_bundles):
    validate_url = '{rosetta_url}/content/custom/{repo_rid}/validate'.format(rosetta_url=get_rosetta_url(),
                                                                                   repo_rid=get_repo_rid())
    payload = {'allowedWords': allowed_words, 'docsBundles': docs_bundles}

    try:
        response = post_request(validate_url, payload, get_token())
    except Exception as e:
        raise RuntimeError("Failed to retrieve validation status.", e)
    try:
        validate_response = json.load(response)
    except TypeError:
        validate_response = json.loads(response.read())
    return validate_response['errors']


def publish(allowed_words, docs_bundles):
    publish_url = '{rosetta_url}/content/custom/{repo_rid}'.format(rosetta_url=get_rosetta_url(),
                                                                   repo_rid=get_repo_rid())
    payload = {'allowedWords': allowed_words, 'docsBundles': docs_bundles}

    try:
        put_request(publish_url, payload, get_token())
    except Exception as e:
        raise RuntimeError("Failed to publish documentation.", e)

def validate_aip_assist_file(aip_config, product_ids):
    invalid_ids = set(aip_config.keys()).difference(product_ids)
    if invalid_ids:
        raise RuntimeError("Invalid product ids found in _aip-assist.json: {}"
                           .format(invalid_ids))


def get_docs_bundle_with_aip_publication(product_id, files, aip_assist_file):
    if product_id in aip_assist_file:
        return {'productId': product_id, 'files': files, 'aipAssistMetadata': aip_assist_file[product_id]}
    return get_docs_bundle(product_id, files)


def get_docs_bundle(product_id, files):
    return {'productId': product_id, 'files': files}


def get_docs_bundles_with_aip_publication(product_files, aip_assist_metadata):
    return [get_docs_bundle_with_aip_publication(product_id, files, aip_assist_metadata) for product_id, files in product_files.items()]


def get_docs_bundles(product_files):
    return [get_docs_bundle(product_id, files) for product_id, files in product_files.items()]


### RUNNING SCRIPT ###
if get_security_mode() != 'SECURE_MODE':
    raise RuntimeError("Repository is not in SECURE_MODE. Please override the Security Mode for this repo in Jemma's configuration.")

print('Compiling files from repository.')
project_files = get_file_payload()
aip_assist_file = get_aip_asist_file_payload() if contains_aip_assist_file() else None
if aip_assist_file:
    print('Found aip-assist.json file. Attempting to publish configured docs bundles to AIP Assist')
    validate_aip_assist_file(aip_assist_file, set(project_files.keys()))
    docs_bundles = get_docs_bundles_with_aip_publication(project_files, aip_assist_file)
else:
    docs_bundles = get_docs_bundles(project_files)
allowed_words = get_allowed_words()

print
print('Validating docs bundles from repository:')
print('\n'.join(project_files.keys()))

errors = validate(allowed_words, docs_bundles)
if len(errors) > 0:
    print('\n-----BUNDLE ERRORS-----')
    pretty_print_errors(errors)
    if len(get_error_level_errors(errors)) > 0:
        raise RuntimeError('Found errors in your bundle.')
    else:
        print('Found warnings in your bundle.')
else:
    print('All docs bundles are error-free!')

if get_branch() == 'master':
    print('\nOn master branch. Attempting to publish bundles...')
    publish(allowed_words, docs_bundles)
    print('Successfully queued docs for update. Changes may take up to an hour to be processed.')
