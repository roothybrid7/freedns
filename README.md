======================================
 Dynamic DNS Client (FreeDNS XML API)
======================================

FreeDNS: http://freedns.afraid.org/ で用意されているXML APIから、Dynamic DNS更新用URLを取得してDNSのレコードを更新するスクリプトです。


Quick-start
===========

スクリプトディレクトリをダウンロードし、任意の場所に配置する。

下記のコマンドをFreeDNSの登録ユーザ名を指定し実行する。

    $ cd [script directory]
    $ python freednsupdate.py -u [FreeDNSの登録ユーザ名]
    Password: <- 登録ユーザのパスワードを入力

freednsupdate.py
================

実行オプション
--------------

.. code-block:: bash

    $ python freednsupdate.py -h
    Usage: freednsupdate.py [options]

    Options:
      -u USERNAME, --user=USERNAME
                            Username of FreeDNS domain hosting
      -p PASSWORD, --pass=PASSWORD
                            User password of FreeDNS domain hosting
      -v, --verbose
      -q, --quiet
      --version             show program's version number and exit
      -h, --help            show this help message and exit


実行サンプル
------------

ユーザ名とパスワードを指定してレコードを更新する。

.. code-block:: bash

  $ python freednsupdate.py -u hoge -p password [OR -username=hoge --password=password]

ユーザ名のみ指定して、パスワードは画面上に出力させないようパスワードプロンプトで入力して更新する。

.. code-block:: bash

  $ python freednsupdate.py -u hoge [OR --username=hoge]
  Password:

実行オプション未指定でレコードを更新する。(ユーザ名とパスワードを指定して作成する暗号化文字列を保存した設定ファイルが必要: 後述)

.. code-block:: bash

  $ python freednsupdate.py


cronなどで定期敵に実行したい場合
--------------------------------

ユーザ名とパスワードを指定して作成する暗号化文字列を保存した設定ファイルが必要: 後述)

1時間おきに実行したい場合

.. code-block:: bash

  $ crontab -l
  0 * * * * python /home/hoge/cron/freedns/freednsupdate.py


loadconfig.py
=============

このファイルをスクリプトとして実行すると、ユーザ名をパスワードを指定して作成する暗号化文字列を保存した設定ファイルを作成する。
(設定ファイル名は、settings.pyの


実行オプション
--------------

.. code-block:: bash

  $ python loadconfig.py -h
  Usage: loadconfig.py [options]

  Options:
    -h, --help            show this help message and exit
    -u USERNAME, --username=USERNAME
    -p PASSWORD, --password=PASSWORD

実行サンプル
------------

ユーザ名を指定して実行する。

.. code-block:: bash

  $ python loadconfig.py -u hoge [OR --username=hoge]
  Password:

ユーザ名とパスワードを指定して実行する。

.. code-block:: bash

  $ python loadconfig.py -u hoge -p password [OR --username=hoge --password=password]

settings.py
===========

スクリプトの設定値を指定する

設定値

SECRET
  ユーザ名とパスワードを指定して作成した暗号化文字列を保存する設定ファイル名(デフォルト: [script directory/.freednssec.cfg])

  作成される暗号化文字列は"username|password"(username + pipe + password)をsha1で暗号化してもの

SECTION
  設定ファイル名のセクション名(デフォルト: Secret)

HASH_ARGO
  URLパラメータで指定する暗号化方式(URLパラメータ: ?sha=xxxxx[暗号化文字列])

  暗号化方式自体は、sha-1

TARGET_PARAMS
  URLパラメータのキーと値(HASH_ARGOの部分はユーザ名とパスワードにより動的に決定する)

TARGET_API
  FreeDNSのXML APIを取得するURL

TIMEOUT
  XML API取得とDynamic DNS update実行時のタイムアウト値(デフォルト: 300秒)

settings.py
.. code-block:: python

  #!/usr/bin/env python
  # -*- coding:utf-8 -*-

  import os
  import sys 
  import traceback

  BASE_DIR = os.path.dirname(os.path.abspath(__file__))

  # User account and api settings
  SECRET = os.path.join(BASE_DIR, ".freednssec.cfg")
  SECTION = "Secret"
  HASH_ARGO = "sha"
  TARGET_PARAMS = {'action': "getdyndns", HASH_ARGO: None, 'style': "xml"}
  TARGET_API = "http://freedns.afraid.org/api/"
  TIMEOUT = 300 

  # Command Options
  VERSION = "%prog 0.1"

  from optparse import make_option
  CMD_OPTIONS = [ 
      make_option("-u", "--user", dest="username",
          help="Username of FreeDNS domain hosting"),
      make_option("-p", "--pass", dest="password",
          help="User password of FreeDNS domain hosting"),
      make_option("-v", "--verbose",
          action="store_true", dest="verbose"),
      make_option("-q", "--quiet",
          action="store_false", dest="verbose"),
  ]


  def verbose(flag):
      if not flag:
          sys.stdout = open(os.devnull)

ユーザ名とパスワードから生成される設定ファイル
==============================================

FreeDNSのXML APIを取得する際に必要な暗号化文字列を保存する設定ファイル

デフォルトの場合
  セクション: Secret

  暗号化文字列項目名: sha

..code-block:: cfg

  [Secret]
  sha = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


