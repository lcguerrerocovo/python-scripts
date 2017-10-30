#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import csv
import argparse
import sys

github_url = 'https://api.github.com'

def get_repos(paging_url,credentials):
    sys.stdout.write("\r fetching repositories ...")
    r = requests.get(paging_url, auth=(credentials[0],credentials[1]))
    sys.stdout.flush()
    if not('next' in r.links):
        return r.json()
    else:
        return r.json() + get_repos(r.links['next']['url'],credentials)


def get_teams(repos,credentials):
    for i in range(0,len(repos)):
        sys.stdout.write(("\r fetching repository teams %d of "
            + str(len(repos)) + " ...") % (i+1))
        r = requests.get(repos[i]['teams_url'], auth=(credentials[0],credentials[1]))
        teams = r.json()
        sys.stdout.flush()

        headers = {'Accept' : 'application/vnd.github.v3.repository+json'}
        team_permissions = []
        repos[i]['team_permissions'] = {'owner':[],'write':[],'read':[]}
        for j in range(0,len(teams)):
            url = github_url + "/" + "/".join(["teams", str(teams[j]['id']), "repos", organization, repos[i]['name']])
            r = requests.get(url, headers = headers, auth=(credentials[0],credentials[1]))
            response = r.json()
            if 'permissions' in response:
                if response['permissions']['admin'] == True:
                    repos[i]['team_permissions']['owner'].append(teams[j]['name'])
                elif response['permissions']['push'] == True:
                    repos[i]['team_permissions']['write'].append(teams[j]['name'])
                elif response['permissions']['pull'] == True:
                    repos[i]['team_permissions']['read'].append(teams[j]['name'])
    return repos


parser = argparse.ArgumentParser(description='fetch all github repositories \
                            and their respective teams from an organization')
parser.add_argument('organization', type=str,
                   help='organization to fetch repositories from')
parser.add_argument('user', help='github user')
parser.add_argument('password', help='github user password')

args = parser.parse_args()
organization = args.organization
credentials = args.user,args.password

initial_page = github_url + "/orgs/" + organization + "/repos"
repos = get_repos(initial_page,credentials)
repos = get_teams(repos,credentials)


with open(organization + '-repositories.csv', 'wb') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=';')
    csvwriter.writerow(["repository name","url","owner team","write teams","read teams"])
    for i in range(0,len(repos)):
         csvwriter.writerow([repos[i]['name']
            , repos[i]['url'].replace("api.github.com/repos/","github.com/")
            , repos[i]['team_permissions']['owner']
            , repos[i]['team_permissions']['write']
            , repos[i]['team_permissions']['read']])
