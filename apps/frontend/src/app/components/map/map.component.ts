import {Component, AfterViewInit, Input, OnDestroy} from '@angular/core';
import * as L from 'leaflet';
import {Place} from "../../data-model/place";

@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements AfterViewInit, OnDestroy {
  @Input() attractions: Place[][] = [];
  private map: L.Map | undefined;
  icon = {
    icon: L.icon({
      iconSize: [ 25, 41 ],
      iconAnchor: [ 13, 0 ],
      iconUrl: './node_modules/leaflet/dist/images/marker-icon.png',
      shadowUrl: './node_modules/leaflet/dist/images/marker-shadow.png'
    })
  };

  private initMap(): void {
    let totalLat = 0;
    let totalLong = 0;
    let totalCount = 0;

    this.attractions.forEach(day => {
      day.forEach(attraction => {
        totalLat += attraction.latitude;
        totalLong += attraction.longitude;
        totalCount++;
      });
    });

    const averageLat = totalCount > 0 ? totalLat / totalCount : 0;
    const averageLong = totalCount > 0 ? totalLong / totalCount : 0;

    this.map = L.map('map', {
      center: [ averageLat, averageLong ],
      zoom: 12
    });

    const tiles = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 15,
      minZoom: 11,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    });

    tiles.addTo(this.map);

    const colors = ['red',  'blue', 'green', 'orange', 'purple',  'pink', 'lightblue', 'beige']

    const LegendControl = L.Control.extend({
      onAdd: (map: L.Map) => {
        const div = L.DomUtil.create('div', 'info legend');
        let legendHtml = '<h4>Day Index</h4>';
        const colors = ['red', 'blue', 'green', 'orange', 'purple', 'pink', 'lightblue', 'beige'];
        const numberOfDays = this.attractions.length;

        for (let index = 0; index < numberOfDays; index++) {
          legendHtml += `<i style="background: ${colors[index % colors.length]}; width: 18px; height: 18px; float: left; margin-right: 8px; opacity: 0.7;"></i> Day ${index + 1}<br>`;
        }

        div.innerHTML = legendHtml;
        return div;
      },
    });

    const legendControl = new LegendControl({ position: 'bottomright' });
    legendControl.addTo(this.map);

    const customIcon = (day_index: number, attraction_index: number) => L.divIcon({
      className: 'custom-div-icon',
      html: `<div class="marker" style="background: ${colors[day_index]};"><div>${attraction_index+1}</div></div>`,
      iconSize: [100, 50],
      iconAnchor: [50, 25]
    });


    this.attractions.forEach((day, i) => {
      day.forEach((attraction, j) => {
        if (this.map) {
          const marker = L.marker([attraction.latitude, attraction.longitude],
            {icon: customIcon(i,j)}).addTo(this.map);
          marker.bindPopup(`<b>${attraction.name}</b><br>${attraction.formattedAddress}`);
        }
      });
    });

  }

  constructor() { }

  ngAfterViewInit(): void {
    this.initMap();
  }

  ngOnDestroy(): void {
    if (this.map) {
      this.map.off();
      this.map.remove();
    }
  }
}
