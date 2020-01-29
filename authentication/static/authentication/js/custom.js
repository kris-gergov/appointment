jQuery(document).ready(function ($) {
    $('select[name=user_type]').change(function () {
        $("select[name=user_type] option:selected").each(function () {
            var value = $(this).val();
            if (value === "staff") {
                $('#id_school').hide();
                $('#div_id_school').hide();
                $('#id_study_year').hide();
                $('#div_id_study_year').hide();
            } else if (value === "student") {
                $('#id_school').show();
                $('#div_id_school').show();
                $('#id_study_year').show();
                $('#div_id_study_year').show();
            }
        });
    });
});