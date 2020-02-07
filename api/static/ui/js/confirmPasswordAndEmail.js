$(document).ready(function() {
    $('#regconfpassword').blur("input", function() {
        if ($('#regpassword').val() != $('#regconfpassword').val()) {
            $('#passwordtoast').toast('show');
            $(':input[type="submit"]').prop('disabled', true);
        } else {
            $('#passwordtoast').toast('hide');
            $(':input[type="submit"]').prop('disabled', false);
        }
    });
});

$(document).ready(function() {
    $('#regconfemail').blur("input", function() {
        if ($('#regconfemail').val() != $('#regemail').val()) {
            $('#emailtoast').toast('show');
            $(':input[type="submit"]').prop('disabled', true);
        } else {
            $('#emailtoast').toast('hide');
            $(':input[type="submit"]').prop('disabled', false);
        }
    });
});