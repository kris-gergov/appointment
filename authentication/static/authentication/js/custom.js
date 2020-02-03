jQuery(document).ready(function ($) {
    var val = $("#id_user_type").val();
    if (val === "adviser") {
        $('#id_school').hide();
        $('#div_id_school').hide();
        $('#id_study_year').hide();
        $('#div_id_study_year').hide();
        $('#id_booking_slots').show();
        $('#div_id_booking_slots').show();
    } else if (val === "student") {
        $('#id_school').show();
        $('#div_id_school').show();
        $('#id_study_year').show();
        $('#div_id_study_year').show();
        $('#id_booking_slots').hide();
        $('#div_id_booking_slots').hide();
    }

    $('select[name=user_type]').change(function () {
        $("select[name=user_type] option:selected").each(function () {
            var value = $(this).val();
            if (value === "adviser") {
                $('#id_school').hide();
                $('#div_id_school').hide();
                $('#id_study_year').hide();
                $('#div_id_study_year').hide();
                $('#id_booking_slots').show();
                $('#div_id_booking_slots').show();
            } else if (value === "student") {
                $('#id_school').show();
                $('#div_id_school').show();
                $('#id_study_year').show();
                $('#div_id_study_year').show();
                $('#id_booking_slots').hide();
                $('#div_id_booking_slots').hide();
            }
        });
    });
})
;