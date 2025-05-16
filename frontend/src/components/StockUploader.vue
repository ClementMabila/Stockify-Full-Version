<template>
  <div class="stock-upload-panel">
    <!-- File Upload Section -->
    
    <div>
      <div class="upload-section">
      <h4 class="section-title">Stockify helps You Load <div class="heading-span">Your Inventory Stock!</div></h4>
      <!-- File Selection -->
      </div>
      <div class="file-selector">
        <input 
          type="file" 
          ref="fileInput" 
          @change="handleFileSelect" 
          class="file-input" 
          :accept="acceptedFileTypes"
        />
        <div class="file-info" v-if="selectedFile">
          <span class="file-name">{{ selectedFile.name }}</span>
          <span class="file-size">({{ formatFileSize(selectedFile.size) }})</span>
        </div>
      </div>
      
      <!-- Upload Progress -->
      <div v-if="stockUploadStore.isUploading" class="upload-progress">
        <div class="progress-bar">
          <div class="progress-fill" :style="`width: ${stockUploadStore.uploadProgress}%`"></div>
        </div>
        <span class="progress-text">{{ stockUploadStore.uploadProgress }}% Uploaded</span>
      </div>
      
      <!-- Column Mapping (if needed) -->
      <div v-if="stockUploadStore.fileColumns.length > 0 && !stockUploadStore.isUploading" class="column-mapping">
        <h5>Map Columns</h5>
        <p class="mapping-instructions">Map your file columns to the required fields:</p>
        
        <div v-for="(column, index) in stockUploadStore.fileColumns" :key="index" class="column-map-row">
          <div class="file-column">{{ column }}</div>
          <span class="map-arrow">→</span>
          <select v-model="stockUploadStore.mappedColumns[column]" class="mapping-select">
            <option value="">-- Skip this column --</option>
            <option value="name">Product Name</option>
            <option value="sku">SKU</option>
            <option value="category">Category</option>
            <option value="quantity">Quantity</option>
            <option value="unit_price">Unit Price</option>
            <option value="supplier">Supplier</option>
            <option value="available_size">Available Size</option>
            <option value="location">Location</option>
            <option value="reorder_level">Reorder Level</option>
          </select>
        </div>
      </div>
      
      <!-- Action Buttons -->
      <div class="upload-actions">
        <button 
          class="upload-button" 
          @click="uploadFile" 
          :disabled="!selectedFile || stockUploadStore.isUploading"
        >
          Upload Stock Data
        </button>
        
        <div class="template-buttons">
          <button class="template-button" @click="downloadTemplate('csv')">CSV Template</button>
          <button class="template-button" @click="downloadTemplate('xlsx')">Excel Template</button>
        </div>
      </div>
      
      <!-- Error Display -->
      <div v-if="stockUploadStore.uploadError" class="upload-error">
        <p>{{ stockUploadStore.uploadError }}</p>
      </div>
    </div>
    
    <!-- Results Section -->
    <div v-if="stockUploadStore.uploadResults" class="upload-results">
      <h4 class="results-title">Upload Results</h4>
      
      <div class="results-summary">
        <div class="result-item success">
          <span class="result-label">Successfully Processed:</span>
          <span class="result-value">{{ stockUploadStore.uploadResults.success }}</span>
        </div>
        <div class="result-item created">
          <span class="result-label">Products Created:</span>
          <span class="result-value">{{ stockUploadStore.uploadResults.created.length }}</span>
        </div>
        <div class="result-item updated">
          <span class="result-label">Products Updated:</span>
          <span class="result-value">{{ stockUploadStore.uploadResults.updated.length }}</span>
        </div>
        <div v-if="stockUploadStore.uploadResults.errors.length > 0" class="result-item errors">
          <span class="result-label">Errors:</span>
          <span class="result-value">{{ stockUploadStore.uploadResults.errors.length }}</span>
        </div>
      </div>
      
      <!-- Detailed Results -->
      <div v-if="stockUploadStore.uploadResults.created.length > 0" class="result-detail">
        <h5>Created Products</h5>
        <ul class="result-list">
          <li v-for="(sku, index) in stockUploadStore.uploadResults.created" :key="`created-${index}`">
            {{ sku }}
          </li>
        </ul>
      </div>
      
      <div v-if="stockUploadStore.uploadResults.updated.length > 0" class="result-detail">
        <h5>Updated Products</h5>
        <ul class="result-list">
          <li v-for="(sku, index) in stockUploadStore.uploadResults.updated" :key="`updated-${index}`">
            {{ sku }}
          </li>
        </ul>
      </div>
      
      <div v-if="stockUploadStore.uploadResults.errors.length > 0" class="result-detail errors">
        <h5>Errors</h5>
        <ul class="result-list error-list">
          <li v-for="(error, index) in stockUploadStore.uploadResults.errors" :key="`error-${index}`">
            {{ error }}
          </li>
        </ul>
      </div>
      
      <button @click="closeResults" class="close-results-button">Close Results</button>
    </div>
    </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import { useStockUploadStore } from '../store/products';

export default {
  name: 'StockUploader',
  
  setup() {
    const stockUploadStore = useStockUploadStore();
    const fileInput = ref(null);
    const selectedFile = ref(null);
    
    // Compute accepted file types from supported formats
    const acceptedFileTypes = computed(() => {
      return stockUploadStore.supportedFormats
        .map(format => `.${format}`)
        .join(',');
    });
    
    // Handle file selection
    const handleFileSelect = (event) => {
      const file = event.target.files[0];
      if (file) {
        selectedFile.value = file;
        
        // Reset any previous results
        stockUploadStore.resetUploadState();
        
        // Here we would normally call an API to get columns for mapping
        // For now, we'll simulate it for demonstration
        if (file.name.endsWith('.csv')) {
          // In a real implementation, you would read the file and extract headers
          // For demonstration, we'll set some sample columns
          setTimeout(() => {
            stockUploadStore.fileColumns = [
              'Product Name', 'SKU', 'Category', 'Stock', 'Price', 
              'Supplier Name', 'Size', 'Location', 'Min Stock'
            ];
            
            // Set default mappings based on column names
            const mappings = {};
            stockUploadStore.fileColumns.forEach(col => {
              // Set default mappings based on common column names
              if (col.toLowerCase().includes('product') || col.toLowerCase().includes('name')) {
                mappings[col] = 'name';
              } else if (col.toLowerCase().includes('sku') || col.toLowerCase().includes('code')) {
                mappings[col] = 'sku';
              } else if (col.toLowerCase().includes('category')) {
                mappings[col] = 'category';
              } else if (col.toLowerCase().includes('stock') || col.toLowerCase().includes('quantity') || col.toLowerCase() === 'qty') {
                mappings[col] = 'quantity';
              } else if (col.toLowerCase().includes('price') || col.toLowerCase().includes('cost')) {
                mappings[col] = 'unit_price';
              } else if (col.toLowerCase().includes('supplier')) {
                mappings[col] = 'supplier';
              } else if (col.toLowerCase().includes('size')) {
                mappings[col] = 'available_size';
              } else if (col.toLowerCase().includes('location') || col.toLowerCase().includes('warehouse')) {
                mappings[col] = 'location';
              } else if (col.toLowerCase().includes('min') || col.toLowerCase().includes('reorder')) {
                mappings[col] = 'reorder_level';
              } else {
                mappings[col] = ''; // Skip this column by default
              }
            });
            
            stockUploadStore.mappedColumns = mappings;
          }, 500);
        }
      }
    };
    
    // Format file size to human-readable format
    const formatFileSize = (sizeInBytes) => {
      if (sizeInBytes < 1024) {
        return sizeInBytes + ' bytes';
      } else if (sizeInBytes < 1024 * 1024) {
        return (sizeInBytes / 1024).toFixed(2) + ' KB';
      } else {
        return (sizeInBytes / (1024 * 1024)).toFixed(2) + ' MB';
      }
    };
    
    // Upload the file
    const uploadFile = async () => {
      if (!selectedFile.value) return;
      
      try {
        await stockUploadStore.uploadStockFile(
          selectedFile.value, 
          Object.keys(stockUploadStore.mappedColumns).length > 0 
            ? stockUploadStore.mappedColumns 
            : null
        );
        
        // After successful upload, refresh inventory data
        // This assumes you have a method to refresh inventory
        // You might need to emit an event or call a parent method
      } catch (error) {
        console.error('Upload failed:', error);
      }
    };
    
    // Download template in the selected format
    const downloadTemplate = (format) => {
      stockUploadStore.downloadTemplate(format);
    };
    
    // Close results and reset state
    const closeResults = () => {
      stockUploadStore.resetUploadState();
      selectedFile.value = null;
      if (fileInput.value) {
        fileInput.value.value = '';
      }
    };
    
    return {
      stockUploadStore,
      fileInput,
      selectedFile,
      acceptedFileTypes,
      handleFileSelect,
      formatFileSize,
      uploadFile,
      downloadTemplate,
      closeResults
    };
  }
};
</script>

<style scoped>

.heading-span {
    background: linear-gradient(120deg, #dcb5ff, #ffcccc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }

.stock-upload-panel {
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.section-title, .results-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 25px;
  color: #333;
}

.file-selector {
  margin-bottom: 15px;
}

.file-input {
  width: 100%;
  padding: 10px;
  border: 1px dashed #ccc;
  border-radius: 4px;
  margin-bottom: 10px;
}

.file-info {
  display: flex;
  align-items: center;
  margin-top: 5px;
}

.file-name {
  font-weight: 500;
  margin-right: 5px;
}

.file-size {
  color: #666;
  font-size: 0.9em;
}

.upload-progress {
  margin: 15px 0;
}

.progress-bar {
  height: 8px;
  background-color: #eee;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background-color: #4CAF50;
  transition: width 0.3s ease;
}

.progress-text {
  display: block;
  text-align: center;
  margin-top: 5px;
  font-size: 0.9em;
  color: #666;
}

.column-mapping {
  margin: 20px 0;
  padding: 15px;
  background-color: #f9f9f9;
  border-radius: 6px;
}

.mapping-instructions {
  margin-bottom: 10px;
  font-size: 0.9em;
  color: #666;
}

.column-map-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-column {
  width: 40%;
  font-weight: 500;
}

.map-arrow {
  margin: 0 10px;
  color: #888;
}

.mapping-select {
  flex-grow: 1;
  padding: 6px 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.upload-actions {
  display: flex;
  flex-direction: column;
  margin-top: 20px;
}

.upload-button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  margin-bottom: 10px;
}

.upload-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.template-buttons {
  display: flex;
  gap: 10px;
}

.template-button {
  padding: 8px 12px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9em;
}

.upload-error {
  margin-top: 15px;
  padding: 10px;
  background-color: #ffebee;
  border-left: 4px solid #f44336;
  color: #d32f2f;
  border-radius: 4px;
}

.upload-results {
  margin-top: 30px;
  padding: 15px;
  background-color: #f5f5f5;
  border-radius: 6px;
}

.results-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 15px;
  margin-bottom: 20px;
}

.result-item {
  padding: 12px;
  border-radius: 6px;
  background-color: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.result-item.success {
  border-left: 4px solid #4CAF50;
}

.result-item.created {
  border-left: 4px solid #2196F3;
}

.result-item.updated {
  border-left: 4px solid #FF9800;
}

.result-item.errors {
  border-left: 4px solid #F44336;
}

.result-label {
  display: block;
  font-size: 0.9em;
  color: #666;
  margin-bottom: 5px;
}

.result-value {
  font-size: 1.2em;
  font-weight: 600;
}

.result-detail {
  margin-top: 20px;
}

.result-detail h5 {
  font-size: 16px;
  margin-bottom: 10px;
  color: #333;
}

.result-list {
  max-height: 150px;
  overflow-y: auto;
  padding: 10px;
  background-color: white;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.error-list li {
  color: #d32f2f;
}

.close-results-button {
  margin-top: 20px;
  padding: 8px 15px;
  background-color: #f0f0f0;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
}

.file-input {
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 6px;
  width: 100%;
}

.file-info {
  margin-top: 8px;
  font-size: 14px;
  color: #666;
}

.upload-progress {
  margin-top: 10px;
}

.progress-bar {
  background-color: #f0f0f0;
  border-radius: 6px;
  overflow: hidden;
  height: 10px;
  width: 100%;
}

.progress-fill {
  background-color: #4caf50;
  height: 100%;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 12px;
  color: #555;
  margin-top: 4px;
}

.column-mapping {
  margin-top: 20px;
}

.column-map-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

.file-column {
  flex: 1;
  font-weight: 500;
}

.map-arrow {
  margin: 0 10px;
  color: #888;
}

.mapping-select {
  flex: 2;
  padding: 5px;
  border-radius: 4px;
}

.upload-actions {
  margin-top: 20px;
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.upload-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.upload-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.template-buttons {
  display: flex;
  gap: 8px;
}

.template-button {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  padding: 8px 12px;
  border-radius: 4px;
  cursor: pointer;
}

.upload-error {
  margin-top: 15px;
  color: red;
  font-weight: bold;
}

.upload-results {
  margin-top: 30px;
}

.results-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 15px;
}

.result-item {
  font-size: 14px;
}

.result-item.success {
  color: green;
}

.result-item.created {
  color: blue;
}

.result-item.updated {
  color: orange;
}

.result-item.errors {
  color: red;
}

.result-detail {
  margin-top: 15px;
}

.result-list {
  list-style-type: disc;
  margin-left: 20px;
}

.error-list {
  color: red;
}

.close-results-button {
  margin-top: 20px;
  padding: 10px 16px;
  border: none;
  background-color: #888;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

/* File Selection Area */
.file-selector {
  background: linear-gradient(145deg, #f0f0f0, #ffffff);
  border: 1px dashed #dcb5ff;
  border-radius: 16px;
  padding: 30px;
  margin-bottom: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
  position: relative;
}

.file-selector:hover {
  border-color: #6c5ce7;
  transform: translateY(-3px);
  box-shadow: 0 8px 15px rgba(108, 92, 231, 0.1);
}

.file-input {
  width: 100%;
  height: 100%;
  opacity: 0;
  position: absolute;
  top: 0;
  left: 0;
  cursor: pointer;
  z-index: 10;
}

.file-selector::before {
  content: 'Choose a file or drag it here';
  position: absolute;
  font-size: 12px;
   background: linear-gradient(120deg, #dcb5ff, #ffcccc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  pointer-events: none;
}

.file-info {
  margin-top: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: rgba(108, 92, 231, 0.1);
  padding: 12px 24px;
  border-radius: 12px;
  width: 100%;
  text-align: center;
}

.file-name {
  font-weight: bold;
  color: #6c5ce7;
  font-size: 16px;
}

.file-size {
  color: #777;
  font-size: 14px;
  margin-top: 5px;
}

/* Upload Progress */
.upload-progress {
  margin-bottom: 30px;
}

.progress-bar {
  height: 12px;
  background: #eee;
  border-radius: 6px;
  overflow: hidden;
  margin-bottom: 10px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #00c9ff, #92fe9d);
  border-radius: 6px;
  transition: width 0.3s ease;
}

.progress-text {
  font-size: 14px;
  color: #555;
  text-align: right;
}

/* Column Mapping */
.column-mapping {
  background: white;
  border-radius: 16px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.column-mapping h5 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
}

.mapping-instructions {
  font-size: 14px;
  color: #666;
  margin-bottom: 20px;
}

.column-map-row {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  padding: 10px;
  background: #f9f9f9;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.column-map-row:hover {
  background: #f0f0f0;
}

.file-column {
  flex: 1;
  font-weight: 500;
  color: #444;
}

.map-arrow {
  margin: 0 15px;
  color: #aaa;
  font-size: 16px;
}

.mapping-select {
  flex: 1.5;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: white;
  color: #555;
  transition: all 0.2s ease;
}

.mapping-select:focus {
  border-color: #6c5ce7;
  box-shadow: 0 0 0 3px rgba(108, 92, 231, 0.2);
  outline: none;
}

/* Action Buttons */
.upload-actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.upload-button {
  padding: 16px 30px;
  background: linear-gradient(135deg, #6c5ce7, #a29bfe);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 15px rgba(108, 92, 231, 0.3);
  display: flex;
  align-items: center;
  justify-content: center;
}

.upload-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(108, 92, 231, 0.4);
  background: linear-gradient(135deg, #5d4cd3, #917ef9);
}

.upload-button:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.template-buttons {
  display: flex;
  gap: 15px;
}

.template-button {
  flex: 1;
  padding: 7px 7px;
  background: white;
  color: #dcb5ff;
  border: 1px solid #dcb5ff;
  border-radius: 12px;
  font-size: 11px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}

.template-button:hover {
  background: rgba(108, 92, 231, 0.1);
  transform: translateY(-2px);
}

/* Error Display */
.upload-error {
  background: #ffecf0;
  border-left: 4px solid #ff5b8d;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.upload-error p {
  color: #d63031;
  margin: 0;
  font-size: 14px;
}

/* Right Side - Results Section */
.upload-results {
  flex: 1;
  padding: 40px;
  background: #fff;
  overflow-y: auto;
  animation: fadeIn 0.5s ease-out;
  position: relative;
  background: linear-gradient(145deg, #ffffff, #f9f9f9);
}

.upload-results::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 10px;
  background: linear-gradient(90deg, #92fe9d, #00c9ff);
}

.results-title {
  font-size: 28px;
  margin-bottom: 30px;
  color: #333;
  font-weight: 700;
  position: relative;
  display: inline-block;
}

.results-title::after {
  content: '';
  position: absolute;
  bottom: -8px;
  left: 0;
  width: 60px;
  height: 4px;
  background: #00b894;
  border-radius: 2px;
}

/* Results Summary */
.results-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.result-item {
  padding: 20px;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.result-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
}

.result-item.success {
  background: linear-gradient(145deg, #ebfffa, #d7f8ee);
}

.result-item.created {
  background: linear-gradient(145deg, #e6f7ff, #d9efff);
}

.result-item.updated {
  background: linear-gradient(145deg, #eee5ff, #e0d3ff);
}

.result-item.errors {
  background: linear-gradient(145deg, #fff0f3, #ffe6ec);
}

.result-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
}

.result-value {
  font-size: 28px;
  font-weight: 700;
}

.result-item.success .result-value {
  color: #00b894;
}

.result-item.created .result-value {
  color: #0984e3;
}

.result-item.updated .result-value {
  color: #6c5ce7;
}

.result-item.errors .result-value {
  color: #ff5b8d;
}

/* Detailed Results */
.result-detail {
  background: white;
  border-radius: 16px;
  padding: 25px;
  margin-bottom: 25px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.05);
}

.result-detail h5 {
  font-size: 20px;
  margin-bottom: 15px;
  color: #333;
  display: flex;
  align-items: center;
}

.result-detail h5::before {
  content: '✓';
  margin-right: 10px;
  color: #00b894;
  font-size: 18px;
}

.result-detail.errors h5::before {
  content: '!';
  color: #ff5b8d;
}

.result-list {
  list-style: none;
  padding: 0;
  margin: 0;
  max-height: 200px;
  overflow-y: auto;
}

.result-list li {
  padding: 10px 15px;
  border-radius: 8px;
  margin-bottom: 8px;
  background: #f9f9f9;
  font-size: 14px;
  color: #555;
}

.error-list li {
  background: #fff0f3;
  color: #ff5b8d;
  border-left: 3px solid #ff5b8d;
}

.close-results-button {
  padding: 14px 30px;
  background: linear-gradient(135deg, #00b894, #00cec9);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 15px rgba(0, 184, 148, 0.3);
  display: block;
  margin: 20px auto 0;
}

.close-results-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 20px rgba(0, 184, 148, 0.4);
  background: linear-gradient(135deg, #00a08c, #00b8b5);
}

/* Responsive adjustments */
@media (max-width: 1200px) {
  .stock-upload-panel {
    flex-direction: column;
  }
  
  .upload-section, .upload-results {
    border-right: none;
    border-bottom: 1px dashed #ddd;
  }
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    height: 95%;
    border-radius: 16px;
  }
  
  .upload-section, .upload-results {
    padding: 20px;
  }
  
  .results-summary {
    grid-template-columns: 1fr;
  }
  
  .section-title, .results-title {
    font-size: 24px;
  }
}

/* Animation for list items */
@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.result-list li {
  animation: fadeInUp 0.3s ease-out;
  animation-fill-mode: both;
}

.result-list li:nth-child(1) { animation-delay: 0.1s; }
.result-list li:nth-child(2) { animation-delay: 0.2s; }
.result-list li:nth-child(3) { animation-delay: 0.3s; }
.result-list li:nth-child(4) { animation-delay: 0.4s; }
.result-list li:nth-child(5) { animation-delay: 0.5s; }
/* Add more delays if needed */

/* Fun effects and extras */
.upload-button, .close-results-button {
  position: relative;
  overflow: hidden;
  font-size: 11px;
  font-weight: lighter;
}

.upload-button::after, .close-results-button::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, 
    rgba(255,255,255,0) 0%, 
    rgba(255,255,255,0.2) 50%, 
    rgba(255,255,255,0) 100%);
  transition: all 0.6s ease;
  font-size: 11px;
}

.upload-button:hover::after, .close-results-button:hover::after {
  left: 100%;
}

</style>