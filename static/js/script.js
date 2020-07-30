$(function() {

  // function to create slider ticks
  var setSliderTicks = function() {
    // slider element
    var $slider = $('.slider');
    var max = $slider.slider("option", "max");
    var min = $slider.slider("option", "min");
    var step = $slider.slider("option", "step");
    var spacing = 100 / (max - min);
    // tick element
    var ticks = $slider.find('div.ticks');

    // remove all ticks if they exist
    $slider.find('.ui-slider-tick-mark-main').remove();
    $slider.find('.ui-slider-tick-mark-text').remove();
    $slider.find('.ui-slider-tick-mark-side').remove();

    // generate ticks
    for (var i = min; i <= max; i = i + step) {

      // main ticks (whole number)
      if (i % 1 === 0) {
        $('<span class="ui-slider-tick-mark-main"></span>').css('left', (spacing * i) + '%').appendTo(ticks);
        $('<span class="ui-slider-tick-mark-text">' + i + '</span>').css('left', (spacing * i) + '%').appendTo(ticks);
      }
      // side ticks
      else {
        $('<span class="ui-slider-tick-mark-side"></span>').css('left', (spacing * i) + '%').appendTo(ticks);
      }
    }
  };

  // create slider
  $('#slider').slider({
    // set min and maximum values
    // day hours in this example
    min: 0,
    max: 100,
    // step
    // quarter of an hour in this example
    step: 1.00,
    // range
    range: false,
    // show tooltips
    tooltips: true,
    // current data
    handles: [{
      value: 25,
      type: "person_name"
    }, {
      value: 50,
      type: "address"
    }, {
      value: 75,
      type: "city"
    }, {
      value: 100,
      type: "zip"
    }],
    // display type names
    showTypeNames: true,
    typeNames: {
      'person_name': 'Person Name',
      'address': 'Address',
      'city': 'City',
      'zip': 'Zip'
    },
    // main css class (of unset data)
    mainClass: 'zip',
    // slide callback
    slide: function(e, ui) {
      console.log(e, ui);
    },
    // handle clicked callback
    handleActivated: function(event, handle) {
      // get select element
      var select = $(this).parent().find('.slider-controller select');
      // set selected option
      select.val(handle.type);
    }

  });

  // button for adding new ranges
  $('.slider-controller button.add').click(function(e) {
      e.preventDefault();
      // get slider
      var $slider = $('#slider');
      // trigger addHandle event
      $slider.slider('addHandle', {
        value: 12,
        type: $('.slider-controller select').val()
      });
      return false;
    });

  // button for removing currently selected handle
  $('.slider-controller button.remove').click(function(e) {
      e.preventDefault();
      // get slider
      var $slider = $('#slider');
      // trigger removeHandle event on active handle
      $slider.slider('removeHandle', $slider.find('a.ui-state-active').attr('data-id'));

      return false;
    });

  // when clicking on handler
  $(document).on('click', '.slider a', function() {
    var select = $('.slider-controller select');
    // enable if disabled
    //select.attr('disabled', false);
    alert($(this).attr('data-type'));
    select.val($(this).attr('data-type'));
    /*if ($(this).parent().find('a.ui-state-active').length)
      $(this).toggleClass('ui-state-active');*/
  });
});
