export const kpiData = {
  totalCarbon: { value: 12847, unit: "tons", change: -3.2 },
  aqi: { value: 72, unit: "AQI", change: 5.1 },
  energyUsage: { value: 458320, unit: "kWh", change: -1.8 },
  fuelConsumption: { value: 34250, unit: "liters", change: 2.4 },
  sustainabilityScore: { value: 78, unit: "%", change: 4.5 },
};

export const emissionTrends = [
  { month: "Jan", co2: 1850, ch4: 120, n2o: 45 },
  { month: "Feb", co2: 1720, ch4: 115, n2o: 42 },
  { month: "Mar", co2: 1680, ch4: 108, n2o: 38 },
  { month: "Apr", co2: 1590, ch4: 102, n2o: 35 },
  { month: "May", co2: 1520, ch4: 98, n2o: 33 },
  { month: "Jun", co2: 1480, ch4: 95, n2o: 31 },
  { month: "Jul", co2: 1450, ch4: 92, n2o: 30 },
  { month: "Aug", co2: 1390, ch4: 88, n2o: 28 },
  { month: "Sep", co2: 1350, ch4: 85, n2o: 27 },
  { month: "Oct", co2: 1320, ch4: 82, n2o: 25 },
  { month: "Nov", co2: 1280, ch4: 80, n2o: 24 },
  { month: "Dec", co2: 1250, ch4: 78, n2o: 22 },
];

export const energyData = [
  { month: "Jan", renewable: 12500, nonRenewable: 28500 },
  { month: "Feb", renewable: 13200, nonRenewable: 27800 },
  { month: "Mar", renewable: 14800, nonRenewable: 26500 },
  { month: "Apr", renewable: 16200, nonRenewable: 25200 },
  { month: "May", renewable: 17800, nonRenewable: 24100 },
  { month: "Jun", renewable: 19500, nonRenewable: 23000 },
  { month: "Jul", renewable: 20800, nonRenewable: 22200 },
  { month: "Aug", renewable: 21500, nonRenewable: 21800 },
  { month: "Sep", renewable: 22200, nonRenewable: 21000 },
  { month: "Oct", renewable: 23000, nonRenewable: 20500 },
  { month: "Nov", renewable: 23800, nonRenewable: 20000 },
  { month: "Dec", renewable: 24500, nonRenewable: 19500 },
];

export const fuelData = [
  { name: "Diesel", value: 45, cost: 52000 },
  { name: "Petrol", value: 25, cost: 31000 },
  { name: "Natural Gas", value: 30, cost: 18000 },
];

export const fuelMonthly = [
  { month: "Jan", diesel: 3200, petrol: 1800, gas: 2100 },
  { month: "Feb", diesel: 3100, petrol: 1750, gas: 2050 },
  { month: "Mar", diesel: 2900, petrol: 1700, gas: 1980 },
  { month: "Apr", diesel: 2800, petrol: 1650, gas: 1900 },
  { month: "May", diesel: 2700, petrol: 1600, gas: 1850 },
  { month: "Jun", diesel: 2650, petrol: 1550, gas: 1800 },
];

export const airQualityData = {
  aqi: 72,
  pm25: 35.2,
  pm10: 58.4,
  co: 0.8,
  no2: 22.5,
  so2: 8.3,
};

export const carbonEmissionRecords = [
  { id: "1", date: "2024-01-15", unit: "Plant A", co2: 450, ch4: 28, n2o: 12, total: 490 },
  { id: "2", date: "2024-01-15", unit: "Plant B", co2: 380, ch4: 22, n2o: 9, total: 411 },
  { id: "3", date: "2024-02-15", unit: "Plant A", co2: 420, ch4: 25, n2o: 11, total: 456 },
  { id: "4", date: "2024-02-15", unit: "Plant C", co2: 310, ch4: 18, n2o: 7, total: 335 },
  { id: "5", date: "2024-03-15", unit: "Plant B", co2: 360, ch4: 20, n2o: 8, total: 388 },
  { id: "6", date: "2024-03-15", unit: "Plant A", co2: 400, ch4: 24, n2o: 10, total: 434 },
  { id: "7", date: "2024-04-15", unit: "Plant C", co2: 290, ch4: 16, n2o: 6, total: 312 },
  { id: "8", date: "2024-04-15", unit: "Plant B", co2: 340, ch4: 19, n2o: 8, total: 367 },
];

export const recentActivities = [
  { id: 1, action: "Carbon emission report generated", user: "Sarah Chen", time: "2 min ago", type: "report" },
  { id: 2, action: "AQI threshold alert triggered", user: "System", time: "15 min ago", type: "alert" },
  { id: 3, action: "Energy data updated for Plant A", user: "James Wilson", time: "1 hr ago", type: "update" },
  { id: 4, action: "New fuel consumption entry added", user: "Priya Sharma", time: "2 hrs ago", type: "entry" },
  { id: 5, action: "Sustainability score improved", user: "System", time: "3 hrs ago", type: "success" },
];
