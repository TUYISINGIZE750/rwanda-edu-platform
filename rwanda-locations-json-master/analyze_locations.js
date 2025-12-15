const fs = require('fs');

function analyzeRwandaLocations() {
    const data = JSON.parse(fs.readFileSync('locations.json', 'utf8'));
    
    // Count all levels
    const provinces = data.provinces.length;
    const districts = data.provinces.reduce((sum, p) => sum + p.districts.length, 0);
    const sectors = data.provinces.reduce((sum, p) => 
        sum + p.districts.reduce((dSum, d) => dSum + d.sectors.length, 0), 0);
    const cells = data.provinces.reduce((sum, p) => 
        sum + p.districts.reduce((dSum, d) => 
            dSum + d.sectors.reduce((sSum, s) => sSum + s.cells.length, 0), 0), 0);
    const villages = data.provinces.reduce((sum, p) => 
        sum + p.districts.reduce((dSum, d) => 
            dSum + d.sectors.reduce((sSum, s) => 
                sSum + s.cells.reduce((cSum, c) => cSum + c.villages.length, 0), 0), 0), 0);
    
    console.log('🇷🇼 RWANDA COMPLETE ADMINISTRATIVE STRUCTURE');
    console.log('='.repeat(50));
    console.log(`📍 Provinces: ${provinces}`);
    console.log(`📍 Districts: ${districts}`);
    console.log(`📍 Sectors: ${sectors}`);
    console.log(`📍 Cells: ${cells}`);
    console.log(`📍 Villages: ${villages}`);
    console.log(`📍 Total Administrative Units: ${villages + cells + sectors + districts + provinces}`);
    
    return { data, stats: { provinces, districts, sectors, cells, villages } };
}

function searchLocation(data, searchTerm) {
    const results = [];
    
    data.provinces.forEach(province => {
        province.districts.forEach(district => {
            district.sectors.forEach(sector => {
                sector.cells.forEach(cell => {
                    cell.villages.forEach(village => {
                        if (village.name.toLowerCase().includes(searchTerm.toLowerCase())) {
                            results.push({
                                village: village.name,
                                cell: cell.name,
                                sector: sector.name,
                                district: district.name,
                                province: province.name,
                                fullPath: `${village.name} → ${cell.name} → ${sector.name} → ${district.name} → ${province.name}`
                            });
                        }
                    });
                });
            });
        });
    });
    
    return results;
}

function getAllLocations(data) {
    const allLocations = {
        provinces: [],
        districts: [],
        sectors: [],
        cells: [],
        villages: []
    };
    
    data.provinces.forEach(province => {
        allLocations.provinces.push(province.name);
        
        province.districts.forEach(district => {
            allLocations.districts.push({
                name: district.name,
                province: province.name
            });
            
            district.sectors.forEach(sector => {
                allLocations.sectors.push({
                    name: sector.name,
                    district: district.name,
                    province: province.name
                });
                
                sector.cells.forEach(cell => {
                    allLocations.cells.push({
                        name: cell.name,
                        sector: sector.name,
                        district: district.name,
                        province: province.name
                    });
                    
                    cell.villages.forEach(village => {
                        allLocations.villages.push({
                            name: village.name,
                            cell: cell.name,
                            sector: sector.name,
                            district: district.name,
                            province: province.name
                        });
                    });
                });
            });
        });
    });
    
    return allLocations;
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        analyzeRwandaLocations,
        searchLocation,
        getAllLocations
    };
}

// Run analysis if called directly
if (require.main === module) {
    const { data, stats } = analyzeRwandaLocations();
    
    console.log('\n🔍 Example: Search for "Kigali"');
    const results = searchLocation(data, 'Kigali').slice(0, 5);
    results.forEach(r => console.log(`   ${r.fullPath}`));
    
    console.log(`\n✅ Analysis complete! All ${stats.villages} villages from ${stats.provinces} provinces are available.`);
}