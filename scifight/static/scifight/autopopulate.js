(function($) {
    /* This script is injected into Django admin HTML code to enable automatic
       short name generation for participants, leaders and jury. It treats all
       text before a comma as last name, and the first word after the comma is
       counted as first name.

       Example conversions:

          Uskov, Grigory Konstantinovich   -> Grigory Uskov
          Soryu, Asuka Langley             -> Asuka Soryu
          Saint-Exupéry, Antoine           -> Antoine Saint-Exupéry

       This behavior mimics how BibTeX normalizes and converts names, and may
       give suboptimal results sometimes. */

    var prevFullName = "";

    function convertName(fullName) {
        var match = /^\s*([^,]+?)\s*,\s*(\S+)/.exec(fullName);
        if (!match)
            return '';

        var lastName  = match[1];
        var firstName = match[2];
        return firstName + ' ' + lastName;
    }

    $(window).on("load", function() {

        var $shortName = $('#id_short_name');
        var $fullName  = $('#id_full_name');

        prevFullName = $shortName.val();

        $fullName.on('focusin', function(){
            prevFullName = $fullName.val();
        });

        $fullName.on('change', function(){
            var shortName = $shortName.val();
            if (shortName == '' || shortName == convertName(prevFullName)) {
                var convertedName = convertName($fullName.val());
                if (convertedName)
                    $shortName.val(convertedName);
            }
        });
    });
})(django.jQuery);
