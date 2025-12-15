/**
 * Rwanda Locations Module
 * Handles all Rwanda administrative location functionality
 */
class RwandaLocations {
    constructor() {
        this.data = null;
        this.selectors = {
            province: '#province',
            district: '#district',
            sector: '#sector',
            cell: '#cell',
            village: '#village'
        };
    }

    // Initialize the module
    async init(dataPath = 'locations.json') {
        try {
            await this.loadData(dataPath);
            this.setupEventListeners();
            this.populateProvinces();
            console.log('✅ Rwanda Locations initialized successfully');
        } catch (error) {
            console.error('❌ Failed to initialize Rwanda Locations:', error);
        }
    }

    // Load locations data
    async loadData(dataPath) {
        const response = await fetch(dataPath);
        this.data = await response.json();
    }

    // Setup event listeners for cascading dropdowns
    setupEventListeners() {
        document.querySelector(this.selectors.province)?.addEventListener('change', (e) => {
            if (e.target.value) this.populateDistricts(e.target.value);
        });

        document.querySelector(this.selectors.district)?.addEventListener('change', (e) => {
            const province = document.querySelector(this.selectors.province).value;
            if (e.target.value && province) this.populateSectors(province, e.target.value);
        });

        document.querySelector(this.selectors.sector)?.addEventListener('change', (e) => {
            const province = document.querySelector(this.selectors.province).value;
            const district = document.querySelector(this.selectors.district).value;
            if (e.target.value && province && district) this.populateCells(province, district, e.target.value);
        });

        document.querySelector(this.selectors.cell)?.addEventListener('change', (e) => {
            const province = document.querySelector(this.selectors.province).value;
            const district = document.querySelector(this.selectors.district).value;
            const sector = document.querySelector(this.selectors.sector).value;
            if (e.target.value && province && district && sector) {
                this.populateVillages(province, district, sector, e.target.value);
            }
        });
    }

    // Populate provinces dropdown
    populateProvinces() {
        const select = document.querySelector(this.selectors.province);
        if (!select || !this.data) return;

        select.innerHTML = '<option value="">Select Province</option>';
        this.data.provinces.forEach(province => {
            const option = document.createElement('option');
            option.value = province.name;
            option.textContent = province.name;
            select.appendChild(option);
        });
    }

    // Populate districts dropdown
    populateDistricts(provinceName) {
        const districtSelect = document.querySelector(this.selectors.district);
        const sectorSelect = document.querySelector(this.selectors.sector);
        const cellSelect = document.querySelector(this.selectors.cell);
        const villageSelect = document.querySelector(this.selectors.village);

        this.resetDropdown(districtSelect, 'Select District', false);
        this.resetDropdown(sectorSelect, 'Select Sector', true);
        this.resetDropdown(cellSelect, 'Select Cell', true);
        this.resetDropdown(villageSelect, 'Select Village', true);

        const province = this.data.provinces.find(p => p.name === provinceName);
        if (province) {
            province.districts.forEach(district => {
                const option = document.createElement('option');
                option.value = district.name;
                option.textContent = district.name;
                districtSelect.appendChild(option);
            });
        }
    }

    // Populate sectors dropdown
    populateSectors(provinceName, districtName) {
        const sectorSelect = document.querySelector(this.selectors.sector);
        const cellSelect = document.querySelector(this.selectors.cell);
        const villageSelect = document.querySelector(this.selectors.village);

        this.resetDropdown(sectorSelect, 'Select Sector', false);
        this.resetDropdown(cellSelect, 'Select Cell', true);
        this.resetDropdown(villageSelect, 'Select Village', true);

        const province = this.data.provinces.find(p => p.name === provinceName);
        const district = province?.districts.find(d => d.name === districtName);

        if (district) {
            district.sectors.forEach(sector => {
                const option = document.createElement('option');
                option.value = sector.name;
                option.textContent = sector.name;
                sectorSelect.appendChild(option);
            });
        }
    }

    // Populate cells dropdown
    populateCells(provinceName, districtName, sectorName) {
        const cellSelect = document.querySelector(this.selectors.cell);
        const villageSelect = document.querySelector(this.selectors.village);

        this.resetDropdown(cellSelect, 'Select Cell', false);
        this.resetDropdown(villageSelect, 'Select Village', true);

        const province = this.data.provinces.find(p => p.name === provinceName);
        const district = province?.districts.find(d => d.name === districtName);
        const sector = district?.sectors.find(s => s.name === sectorName);

        if (sector) {
            sector.cells.forEach(cell => {
                const option = document.createElement('option');
                option.value = cell.name;
                option.textContent = cell.name;
                cellSelect.appendChild(option);
            });
        }
    }

    // Populate villages dropdown
    populateVillages(provinceName, districtName, sectorName, cellName) {
        const villageSelect = document.querySelector(this.selectors.village);

        this.resetDropdown(villageSelect, 'Select Village', false);

        const province = this.data.provinces.find(p => p.name === provinceName);
        const district = province?.districts.find(d => d.name === districtName);
        const sector = district?.sectors.find(s => s.name === sectorName);
        const cell = sector?.cells.find(c => c.name === cellName);

        if (cell) {
            cell.villages.forEach(village => {
                const option = document.createElement('option');
                option.value = village.name;
                option.textContent = village.name;
                villageSelect.appendChild(option);
            });
        }
    }

    // Reset dropdown helper
    resetDropdown(select, placeholder, disabled) {
        if (!select) return;
        select.innerHTML = `<option value="">${placeholder}</option>`;
        select.disabled = disabled;
    }

    // Get currently selected location
    getSelectedLocation() {
        return {
            province: document.querySelector(this.selectors.province)?.value || '',
            district: document.querySelector(this.selectors.district)?.value || '',
            sector: document.querySelector(this.selectors.sector)?.value || '',
            cell: document.querySelector(this.selectors.cell)?.value || '',
            village: document.querySelector(this.selectors.village)?.value || ''
        };
    }

    // Search locations
    search(term) {
        if (!this.data || !term) return [];
        
        const results = [];
        const searchTerm = term.toLowerCase();

        this.data.provinces.forEach(province => {
            province.districts.forEach(district => {
                district.sectors.forEach(sector => {
                    sector.cells.forEach(cell => {
                        cell.villages.forEach(village => {
                            if (village.name.toLowerCase().includes(searchTerm)) {
                                results.push({
                                    village: village.name,
                                    cell: cell.name,
                                    sector: sector.name,
                                    district: district.name,
                                    province: province.name,
                                    fullPath: `${village.name}, ${cell.name}, ${sector.name}, ${district.name}, ${province.name}`
                                });
                            }
                        });
                    });
                });
            });
        });

        return results;
    }

    // Validate location path
    validate(provinceName, districtName, sectorName, cellName, villageName) {
        if (!this.data) return false;

        const province = this.data.provinces.find(p => p.name === provinceName);
        if (!province) return false;

        const district = province.districts.find(d => d.name === districtName);
        if (!district) return false;

        const sector = district.sectors.find(s => s.name === sectorName);
        if (!sector) return false;

        const cell = sector.cells.find(c => c.name === cellName);
        if (!cell) return false;

        const village = cell.villages.find(v => v.name === villageName);
        return !!village;
    }

    // Get statistics
    getStats() {
        if (!this.data) return null;

        let provinces = this.data.provinces.length;
        let districts = 0, sectors = 0, cells = 0, villages = 0;

        this.data.provinces.forEach(province => {
            districts += province.districts.length;
            province.districts.forEach(district => {
                sectors += district.sectors.length;
                district.sectors.forEach(sector => {
                    cells += sector.cells.length;
                    sector.cells.forEach(cell => {
                        villages += cell.villages.length;
                    });
                });
            });
        });

        return { provinces, districts, sectors, cells, villages };
    }
}

// Create global instance
window.RwandaLocations = new RwandaLocations();