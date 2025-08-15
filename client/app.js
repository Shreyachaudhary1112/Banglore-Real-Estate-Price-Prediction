// Choose API base automatically:
// - Local dev: http://127.0.0.1:5000
// - Netlify:   /api  (rewritten by client/_redirects to your Render URL)
function apiBase() {
  const host = window.location.hostname;
  const isLocal = host === "127.0.0.1" || host === "localhost";
  return isLocal ? "http://127.0.0.1:5000" : "/api";
}

function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for (var i in uiBathrooms) {
    if (uiBathrooms[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // invalid
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for (var i in uiBHK) {
    if (uiBHK[i].checked) {
      return parseInt(i) + 1;
    }
  }
  return -1; // invalid
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");

  var sqftEl = document.getElementById("uiSqft");
  var uiLocations = document.getElementById("uiLocations");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();

  var sqft = sqftEl ? parseFloat(sqftEl.value) : NaN;
  var location = uiLocations ? uiLocations.value : "";

  if (!Number.isFinite(sqft)) {
    alert("Please enter a valid area in square feet");
    return;
  }
  if (!location) {
    alert("Please select a location");
    return;
  }
  if (bhk <= 0 || bathrooms <= 0) {
    alert("Please choose BHK and Bathroom values");
    return;
  }

  var url = apiBase() + "/predict_home_price";
  var $btn = $(".submit");
  $btn.prop("disabled", true);

  // Server accepts form data or JSON. Keeping form style to match your current code.
  $.post(
    url,
    {
      total_sqft: sqft,
      bhk: bhk,
      bath: bathrooms,
      location: location
    },
    function (data, status) {
      console.log("predict_home_price response:", status, data);
      if (data && typeof data.estimated_price !== "undefined") {
        $("#uiEstimatedPrice").html("<h2>" + data.estimated_price + "</h2>");
      } else {
        $("#uiEstimatedPrice").html("<h2>Could not get price</h2>");
      }
    }
  )
    .fail(function (xhr) {
      console.error("predict_home_price failed:", xhr.status, xhr.responseText);
      $("#uiEstimatedPrice").html("<h2>Request failed. Try again</h2>");
    })
    .always(function () {
      $btn.prop("disabled", false);
    });
}

function onPageLoad() {
  console.log("document loaded");
  var url = apiBase() + "/get_location_names";

  $.get(url, function (data, status) {
    console.log("get_location_names response:", status, data);
    if (data && data.locations) {
      var locations = data.locations;
      var uiLocations = document.getElementById("uiLocations");
      $("#uiLocations").empty();
      for (var i in locations) {
        var opt = new Option(locations[i]);
        $("#uiLocations").append(opt);
      }
    }
  }).fail(function (xhr) {
    console.error("get_location_names failed:", xhr.status, xhr.responseText);
  });
}

window.onload = onPageLoad;
