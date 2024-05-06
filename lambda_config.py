# -*- coding: utf-8 -*-
""" Lambda function (skeleton) for custom AWS Config rule """

__author__ = 'Jonathan Gonzalez'
__date__ = '2022-04-07'

import json
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


try:
	client = boto3.client('config')
except ClientError as e:
	print(e)


def get_current_time():
	now = datetime.now()
	return now.strftime("%Y/%m/%d %H:%M:%S")


def run_manual():
	""" Action pattern for manual evaluation of associated AWS Config rule """
	compliance = 'COMPLIANT'

	# ToDo: add your logic here

	_res_manual = {
		"_resource_id": "",
		"_compliance_type": compliance,
		"_compliance_info": "Manual run"
	}
	return _res_manual


def run_scheduled():
	""" Action pattern for scheduled execution within AWS Config """
	compliance = 'COMPLIANT'

	# ToDo: add your logic here

	_res_scheduled = {
		"_resource_id": "",
		"_compliance_type": compliance,
		"_compliance_info": "Scheduled run"
	}
	return _res_scheduled


def run_changed():
	""" Action pattern for AWS Config detection of a resource change """
	compliance = 'COMPLIANT'

	# ToDo: add your logic here

	_res_changed = {
		"_resource_id": "",
		"_compliance_type": compliance,
		"_compliance_info": "Resource change run"
	}
	return _res_changed


# In AWS Config, an associated Lambda function can get triggered in
# different scenarios. This decision block uses uses a dictionary to
# avoid multiple if/else statements (strategy pattern).
EVENT_ACTION = {
	"Null": run_manual,
	"ScheduledNotification": run_scheduled,
	"ConfigurationItemChangeNotification": run_changed
}


def run_on_event_action(_strategy: str):
	""" Select a destination function for an AWS Config invocation;
	Based on a strategy pattern """
	return EVENT_ACTION[_strategy]()


def lambda_handler(event, context):
	""" This is a Lambda function written in Python 3 """

	local_computer = False if context else True

	invoking_event = event["invokingEvent"]
	nested_event = json.loads(invoking_event)
	message_type = nested_event["messageType"]
	my_return = run_on_event_action(message_type)

	if local_computer:
		# - Printing locally to developer
		result = {
			'ComplianceResourceType': 'AWS::EC2::SecurityGroup',
			'ComplianceResourceId': my_return["_resource_id"],
			'ComplianceType': my_return["_compliance_type"],
			'Annotation': my_return["_compliance_info"],
			'OrderingTimestamp': get_current_time()
		}
		result_json = json.dumps(result)
		print(result_json)
	else:
		# - Sending the evaluation to AWS Config
		client.put_evaluations(
			Evaluations=[
				{
					'ComplianceResourceType': 'AWS::EC2::SecurityGroup',
					'ComplianceResourceId': my_return["_resource_id"],
					'ComplianceType': my_return["_compliance_type"],
					'Annotation': my_return["_compliance_info"],
					'OrderingTimestamp': get_current_time()
				}
			],
			ResultToken=event['resultToken']
		)

	return {
		"message": "task completed"
	}


def main() -> None:
	""" Main function to simulate a real Lambda function;
	In AWS this block does nothing """

	_my_event: dict = {}
	_my_context: dict = {}
	lambda_handler(_my_event, _my_context)


if __name__ == '__main__':
	main()
