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

    var prevFullNames = {};

    function convertName(fullName) {
        var match = /^\s*([^,]+?)\s*,\s*(\S+)/.exec(fullName);
        if (!match)
            return '';

        var lastName  = match[1];
        var firstName = match[2];
        return firstName + ' ' + lastName;
    }

    $(window).on("load", function() {

        $(window).on('focusin', function(event){
            var match = /^(id_[\w_-]*)full_name/.exec(event.target.id);
            if (!match)
                return;

            var midId = match[1];
            prevFullNames[midId] = $('#'+midId+'full_name').val();
        });

        $(window).on('change', function(event){
            var match = /^(id_[\w_-]*)full_name/.exec(event.target.id);
            if (!match)
                return;

            var midId = match[1];
            var $fullName    = $('#'+midId+'full_name');
            var $shortName   = $('#'+midId+'short_name');

            var prevFullName = "";
            if (prevFullNames[midId])
                prevFullName = prevFullNames[midId];

            var shortName = $shortName.val();
            if (shortName == '' || shortName == convertName(prevFullName)) {
                var convertedName = convertName($fullName.val());
                if (convertedName)
                    $shortName.val(convertedName);
            }
        });
    });
})(django.jQuery);
