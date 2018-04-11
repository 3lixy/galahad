class ErrorCodes():
    user = {
        'success': { 'status': 'success', 'result': [0, 'Successfully completed operation.']},
        'invalidOrMissingParameters': { 'status': 'failed', 'result': [1, 'Invalid or missing parameters.']},
        'userNotAuthorized': { 'status': 'failed', 'result': [2, 'The User is not authorized for this operation.']},
        'userTokenExpired': { 'status': 'failed', 'result': [3, 'The provided UserToken has expired. Refresh your session and try again.']},
        'invalidId': { 'status': 'failed', 'result': [10, 'The given ID is invalid.']},
        'userNotAuthorizedForRole': { 'status': 'failed', 'result': [10, 'This User is not authorized to instantiate the given Role.']},
        'invalidVirtueId': { 'status': 'failed', 'result': [10, 'The given Virtue ID is invalid.']},
        'invalidCredentials': { 'status': 'failed', 'result': [11, 'Credentials are not valid for the indicated User.']},
        'virtueAlreadyExistsForRole': { 'status': 'failed', 'result': [11, 'A Virtue already exists for the given User and the given Role.']},
        'virtueAlreadyLaunched': { 'status': 'failed', 'result': [11, 'The indicated Virtue has already been launched.']},
        'virtueAlreadyStopped': { 'status': 'failed', 'result': [11, 'The indicated Virtue is already stopped.']},
        'virtueNotStopped': { 'status': 'failed', 'result': [11, 'The indicated Virtue is not stopped. Please stop it and try again.']},
        'invalidApplicationID': { 'status': 'failed', 'result': [11, 'The given Application ID is invalid.']},
        'userAlreadyLoggedIn': { 'status': 'failed', 'result': [12, 'The given User is already logged into another session. This response is ' +
                'only given if the forceLogoutOfOtherSessions flag was false.']},
        'invalidRoleId': { 'status': 'failed', 'result': [12, 'The given Role ID is not valid.']},
        'virtueStateCannotBeLaunched': { 'status': 'failed', 'result': [12, 'The indicated Virtue is in a state where it cannot be launched. ' +
                'Check the current Virtue state and take necessary actions.']},
        'virtueStateCannotBeStopped': { 'status': 'failed', 'result': [12, 'The indicated Virtue is in a state where it cannot be stopped. ' +
                'Check the current Virtue state and take necessary actions.']},
        'applicationNotInVirtue': { 'status': 'failed', 'result': [12, 'The indicated Application is not in this Virtue/Role.']},
        'userDoesntExist': { 'status': 'failed', 'result': [13, 'The given User does not exist in the system.']},
        'cantEnableTransducers': { 'status': 'failed', 'result': [13, 'One of the configured Transducers can\'t be enabled on this Virtue.']},
        'cantLaunchEnabledTransducers': { 'status': 'failed', 'result': [13, 'One or more of the enabled Transducers can\'t be launched.']},
        'virtueNotRunning': { 'status': 'failed', 'result': [13, 'The Virtue holding this Application is not running. Launch it and try again.']},
        'applicationAlreadyLaunched': { 'status': 'failed', 'result': [14, 'The indicated Application has already been launched.']},
        'resourceCreationError': { 'status': 'failed', 'result': [100, 'There was an error creating the resources for the Virtue. Check ' +
                'user messages and server logs.']},
        'serverLaunchError': { 'status': 'failed', 'result': [100, 'There was an unanticipated server error launched the indicated Virtue. ' +
                'Check user messages for more information.']},
        'serverStopError': { 'status': 'failed', 'result': [100, 'There was an unanticipated server error stopping the indicated Virtue. ' +
                'Check user messages and server logs for more information.']},
        'serverDestroyError': { 'status': 'failed', 'result': [100, 'There was an unanticipated server error destroying the indicated Virtue.' +
                'Check user messages and server logs for more information.']},
        'notImplemented': { 'status': 'failed', 'result': [254, 'This function has not been implemented.']},
        'unspecifiedError': { 'status': 'failed', 'result': [255, 'An otherwise unspecified error. Check user messages and/or error logs ' +
                'for more information.']}
    }
