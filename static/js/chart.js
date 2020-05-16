// var map;

// AmCharts.ready(function () 
// {
//     map = new AmCharts.AmMap();
//     map.panEventsEnabled = true;
//     map.backgroundColor = "#666666";
//     map.backgroundAlpha = 1;

//     map.zoomControl.panControlEnabled = true;
//     map.zoomControl.zoomControlEnabled = true;

//     var dataProvider = {
//         map: "indiaLow",
//         getAreasFromMap: true
//     };

//     map.dataProvider = dataProvider;

//     map.areasSettings = {
//         autoZoom: false,
//         color: "#CDCDCD",
//         colorSolid: "#5EB7DE",
//         selectedColor: "#5EB7DE",
//         outlineColor: "#666666",
//         rollOverColor: "#88CAE7",
//         rollOverOutlineColor: "#FFFFFF",
//         selectable: true
//     };

//     map.addListener("clickMapObject", function (event) 
//     {
//         // deselect the area by assigning all of the dataProvider as selected object
//         map.selectedObject = map.dataProvider;    
    
//         // toggle showAsSelected
//         event.mapObject.showAsSelected = !event.mapObject.showAsSelected;

//         // bring it to an appropriate color
//         map.returnInitialColor(event.mapObject);

//         // let's build a list of currently selected states
//         var states = [];
//         for (var i in map.dataProvider.areas) 
//         {
//             var area = map.dataProvider.areas[i];
//             if (area.showAsSelected) 
//             {
//                 states.push(area.title);
//             }
//         }
//     });

//     map.export = {
//     enabled: true
//   };

//   map.write("chartdiv");
// });


google.load('visualization', '1', {'packages': ['geochart']});
google.setOnLoadCallback(drawVisualization);

function drawVisualization() {
  var data = google.visualization.arrayToDataTable([
        ['State Code', 'State', 'Temperature'],     
          [ 'IN-UP','Uttar Pradesh', 33],
    ['IN-MH','Maharashtra', 32],
    ['IN-BR','Bihar', 31],
    ['IN-WB','West Bengal', 32],
    ['IN-MP','Madhya Pradesh', 30],
    ['IN-TN','Tamil Nadu', 33],
    ['IN-RJ','Rajasthan', 33],
    ['IN-KA','Karnataka', 29],
    ['IN-GJ','Gujarat', 34],
    ['IN-AP','Andhra Pradesh', 32],
    ['IN-OR','Orissa', 33],
    ['IN-TG','Telangana', 33],
    ['IN-KL','Kerala', 31],
    ['IN-JH','Jharkhand', 29],
    ['IN-AS','Assam', 28],
    ['IN-PB','Punjab', 30],
    ['IN-CT','Chhattisgarh', 33],
    ['IN-HR','Haryana', 30],
    ['IN-JK','Jammu and Kashmir', 20],
    ['IN-UT','Uttarakhand', 28],
    ['IN-HP','Himachal Pradesh', 17],
    ['IN-TR','Tripura', 31],
    ['IN-ML','Meghalaya', 21],
    ['IN-MN','Manipur', 22],
    ['IN-NL','Nagaland', 22],
    ['IN-GA','Goa', 32],
    ['IN-AR', 'Arunachal Pradesh', 33],
    ['IN-MZ','Mizoram', 23],
    ['IN-SK','Sikkim', 24],
    ['IN-DL','Delhi', 31],
    ['IN-PY','Puducherry', 33],
    ['IN-CH','Chandigarh', 30],
    ['IN-AN','Andaman and Nicobar Islands', 30],
    ['IN-DN','Dadra and Nagar Haveli', 30],
    ['IN-DD','Daman and Diu', 29],
    ['IN-LD','Lakshadweep', 31]
  ]);

      var opts = {
        region: 'IN',
        domain:'IN',
        displayMode: 'regions',
        colorAxis: {colors: ['#e5ef88', '#d4b114', '#e85a03']},
        resolution: 'provinces',
        /*backgroundColor: '#81d4fa',*/
        /*datalessRegionColor: '#81d4fa',*/
        defaultColor: '#f5f5f5',
        width: 640, 
        height: 480
      };
      var geochart = new google.visualization.GeoChart(
          document.getElementById('visualization'));
      geochart.draw(data, opts);
    };
