#!/usr/bin/env bats

setup() {
    load 'test_helper/_common_setup'
    _common_setup
}

@test "Teardown tmp folder" {
    sudo rm -rf ${PROJET_TMP_FOLDER}
}
