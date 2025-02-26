# Copyright (C) 2023, The HIP team and Contributors, All rights reserved.
#  This software is distributed under the open-source Apache 2.0 license.

"""Test the datahipy CLI "dataset.*" commands."""

from __future__ import absolute_import
import os
import pytest
import json
import datalad
from datalad.support.gitrepo import GitRepo


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_help.py::test_run_help")
def test_run_dataset_create(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "dataset_dirname": "NEW_BIDS_DS",
        "DatasetDescJSON": {
            "Name": "My New BIDS dataset",
            "BIDSVersion": "1.4.0",
            "License": "n/a",
            "Authors": ["Tom", "Jerry"],
            "Acknowledgements": "Overwrite test",
            "HowToAcknowledge": "n/a",
            "Funding": "Picsou",
            "ReferencesAndLinks": "n/a",
            "DatasetDOI": "n/a",
        },
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "create_dataset.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy dataset.create command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "dataset.create",
        "--input_data",
        input_file,
        "--dataset_path",
        os.path.dirname(dataset_path),
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the dataset was created by checking for the dataset_description.json file
    assert os.path.exists(os.path.join(dataset_path, "dataset_description.json"))


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset_create")
def test_run_dataset_create_init_tag(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "path": dataset_path,
        "type": "bids",
        "tag": "0.0.0",
        "changes_list": ["Initial tag at dataset creation"],
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "dataset_create_init_tag.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy dataset.create_tag command
    ret = script_runner.run(
        "datahipy", "--command", "dataset.create_tag", "--input_data", input_file
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the tag was created
    tag_dicts = GitRepo(dataset_path).get_tags()
    assert "0.0.0" in [
        tag_dict["name"] for tag_dict in tag_dicts
    ]


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_sub.py::test_run_sub_import")
def test_run_dataset_create_tag(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "path": dataset_path,
        "type": "bids",
        "tag": "1.0.0",
        "changes_list": ["Import sub-carole data"],
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "dataset_create_tag.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy dataset.create_tag command
    ret = script_runner.run(
        "datahipy", "--command", "dataset.create_tag", "--input_data", input_file
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the tag was created
    tag_dicts = GitRepo(dataset_path).get_tags()
    assert "1.0.0" in [
        tag_dict["name"] for tag_dict in tag_dicts
    ]


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset_create_tag")
def test_run_dataset_get_tags(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "path": dataset_path,
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "dataset_get_tags.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "dataset_get_tags_output.json")
    # Run datahipy dataset.get_tags command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "dataset.get_tags",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the output file was created
    assert os.path.exists(output_file)
    # Load the output json file and check the tag
    with open(output_file, "r") as f:
        output_data = json.load(f)
    assert "1.0.0" in output_data["tags"]
    assert output_data["path"] == dataset_path


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset_get_tags")
def test_run_dataset_get(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {"owner": "hipadmin", "path": dataset_path}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "get_dataset.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "get_dataset_output.json")
    # Run datahipy dataset.get command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "dataset.get",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
        "--dataset_path",
        dataset_path,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the output file was created
    assert os.path.exists(output_file)


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset_get")
def test_run_datasets_get(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "owner": "hipadmin",
        "datasets": [{"path": dataset_path}, {"path": dataset_path}],
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "get_datasets.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "get_datasets_output.json")
    # Run datahipy datasets.get command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "datasets.get",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
    )
    # Check that the command ran successfully
    assert ret.success

@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_datasets_get")
def test_run_dataset_publish(script_runner, dataset_path, public_dataset_path, io_path):
    # Create input data
    input_data = {
        "sourceDatasetPath": dataset_path,
        "targetDatasetPath": public_dataset_path,
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "dataset_publish.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "dataset_publish_output.json")
    # Run datahipy dataset.publish command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "dataset.publish",
        "--input_data",
        input_file,
        "--output_file",
        output_file
    )
    # Check that the command ran successfully
    assert ret.success

@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset_publish")
def test_run_dataset_clone(script_runner, public_dataset_path, cloned_dataset_path, io_path):
    # Create input data
    input_data = {
        "sourceDatasetPath": public_dataset_path,
        "targetDatasetPath": cloned_dataset_path,
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "dataset_clone.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "dataset_clone_output.json")
    # Run datahipy dataset.clone command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "dataset.clone",
        "--input_data",
        input_file,
        "--output_file",
        output_file
    )
    # Check that the command ran successfully
    assert ret.success


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_sub.py::test_run_sub_delete")
def test_run_dataset_release_version(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {
        "path": dataset_path,
        "type": "bids",
        "level": "patch",
        "changes_list": ["Delete sub-carole data"],
    }
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "dataset_release_version.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Output file path
    output_file = os.path.join(io_path, "dataset_release_version_output.json")
    # Run datahipy dataset.release_version command
    ret = script_runner.run(
        "datahipy",
        "--command",
        "dataset.release_version",
        "--input_data",
        input_file,
        "--output_file",
        output_file,
    )
    # Check that the command ran successfully
    assert ret.success
    # Check that the dataset summary JSON output file was created
    assert os.path.exists(output_file)
    # Load the output json file and check the dataset version
    # in the dataset summary JSON output file
    with open(output_file, "r") as f:
        output_data = json.load(f)
    assert "1.0.1" in output_data["DatasetVersion"]


@pytest.mark.script_launch_mode("subprocess")
@pytest.mark.order(after="test_run_dataset_release_version")
def test_run_dataset_checkout_tag(script_runner, dataset_path, io_path):
    # Create input data
    input_data = {"path": dataset_path, "tag": "0.0.0"}
    # Create JSON file path for input data
    input_file = os.path.join(io_path, "dataset_checkout_tag.json")
    # Write input data to file
    with open(input_file, "w") as f:
        json.dump(input_data, f, indent=4)
    # Run datahipy dataset.checkout.tag command
    ret = script_runner.run(
        "datahipy", "--command", "dataset.checkout_tag", "--input_data", input_file
    )
    # Check that the command ran successfully
    assert ret.success
