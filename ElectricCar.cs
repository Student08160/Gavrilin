using System;

namespace MyApp.Models
{
    public class ElectricCar : Car
    {
        private double batteryCapacity;

        public void SetBatteryCapacity(double capacity)
        {
            batteryCapacity = capacity;
        }

        protected override void DisplayInfo()
        {
            base.DisplayInfo();
            Console.WriteLine($"Battery Capacity: {batteryCapacity} кВт/ч");
        }

        public void PublicDisplay()
        {
            DisplayInfo();
        }
    }
}
