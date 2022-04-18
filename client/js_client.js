function get_data(log, bot_name, func_host) {

    $http.config({authService: {

            service: 'platformV',
            app_key: "$credentials.platformV.app_key",
            app_secret: "$credentials.platformV.app_secret",
        }});
    var options = {
        dataType: 'json',
        headers: {
            'Content-Type': 'application/json',
        },
        body: {
        "MESSAGE_NAME": "LOGGER_INFO",
        "DATA": {
            "log_info": log,
            "bot_type": bot_name
        }
    },
    };
    var response = $http.post(func_host, options);

}