document.addEventListener('DOMContentLoaded', function() {
    // Initialize DataTables
    if (document.getElementById('trends-table')) {
        const trendsTable = $('#trends-table').DataTable({
            responsive: true,
            order: [[3, 'desc']], // Sort by popularity score initially
            columnDefs: [
                { responsivePriority: 1, targets: 0 }, // Trend name
                { responsivePriority: 2, targets: 3 }, // Popularity score
                { responsivePriority: 3, targets: 1 }  // Source
            ]
        });
        
        // Add click handler for trends table rows to show details modal
        $('#trends-table tbody').on('click', 'tr', function() {
            const trendName = $(this).data('trend-name');
            const trendSource = $(this).data('trend-source');
            
            // Convert dataset to actual object
            let detailsString = $(this).attr('onclick');
            if (detailsString) {
                try {
                    // Extract the JSON from the onclick attribute
                    const match = detailsString.match(/showTrendDetails\('(.*?)', '(.*?)', (.*)\)/);
                    if (match && match[3]) {
                        const details = JSON.parse(match[3]);
                        showTrendDetails(trendName, trendSource, details);
                    }
                } catch (e) {
                    console.error('Error parsing trend details:', e);
                }
            }
        });
        
        // Add double-click handler for trends table rows to go directly to analysis
        $('#trends-table tbody').on('dblclick', 'tr', function() {
            const trendName = $(this).data('trend-name');
            const trendSource = $(this).data('trend-source');
            if (trendName && trendSource) {
                window.location.href = `/trend/${encodeURIComponent(trendName)}/${encodeURIComponent(trendSource)}`;
            }
        });
        
        // Filter buttons for categories
        document.querySelectorAll('.filter-btn').forEach(button => {
            button.addEventListener('click', function() {
                const filterValue = this.getAttribute('data-filter');
                
                // Toggle active state on buttons
                document.querySelectorAll('.filter-btn').forEach(btn => {
                    btn.classList.remove('active');
                });
                this.classList.add('active');
                
                if (filterValue === 'all') {
                    trendsTable.column(2).search('').draw();
                } else {
                    trendsTable.column(2).search(filterValue).draw();
                }
            });
        });
    }
    
    // Initialize radio button behavior for manual entry form
    if (document.getElementById('manual-entry-form')) {
        // Toggle pop potential selection
        document.querySelectorAll('input[name="pop_potential"]').forEach(input => {
            input.addEventListener('change', function() {
                document.getElementById('pop-potential-yes-label').classList.toggle('active', this.value === 'yes');
                document.getElementById('pop-potential-no-label').classList.toggle('active', this.value === 'no');
            });
        });
    }
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});

// Function to show trend details modal
function showTrendDetails(trendName, source, details) {
    const modal = document.getElementById('trend-details-modal');
    const modalTitle = document.getElementById('trend-details-title');
    const modalBody = document.getElementById('trend-details-body');
    
    // Set the modal title
    modalTitle.textContent = trendName;
    
    // Build the details content based on source
    let detailsHtml = '';
    
    if (source.includes('Google Trends')) {
        detailsHtml = `
            <p><strong>Source:</strong> ${source}</p>
            <p><strong>Category:</strong> ${details.category}</p>
            <p><strong>Region:</strong> ${details.region}</p>
            <p><strong>Type:</strong> ${details.type} trend</p>
            <p><strong>Traffic Score:</strong> ${details.traffic_score}</p>
            <p><strong>Change:</strong> ${details.change > 0 ? '+' + details.change : details.change}</p>
        `;
    } else if (source.includes('Reddit')) {
        detailsHtml = `
            <p><strong>Source:</strong> ${source}</p>
            <p><strong>Score (Upvotes):</strong> ${details.score}</p>
            <p><strong>Link:</strong> <a href="${details.url}" target="_blank" class="text-info">View Original Post</a></p>
            <p><strong>Reddit Thread:</strong> <a href="${details.permalink}" target="_blank" class="text-info">View on Reddit</a></p>
        `;
    } else {
        // Manual entry
        detailsHtml = `
            <p><strong>Source:</strong> ${details.source}</p>
            <p><strong>Category:</strong> ${details.category}</p>
            <p><strong>Lifecycle Stage:</strong> ${details.lifecycle_stage}</p>
            <p><strong>Pop Potential:</strong> ${details.pop_potential ? 'Yes' : 'No'}</p>
            <p><strong>Added:</strong> ${new Date(details.timestamp).toLocaleString()}</p>
            <p><strong>Notes:</strong> ${details.notes || 'No notes provided'}</p>
        `;
    }
    
    // Add button for detailed analysis
    detailsHtml += `
        <div class="mt-4 pt-3 border-top">
            <a href="/trend/${encodeURIComponent(trendName)}/${encodeURIComponent(source)}" class="btn btn-primary w-100">
                <i class="fas fa-chart-line me-2"></i>View In-Depth Analysis & Insights
            </a>
        </div>
    `;
    
    modalBody.innerHTML = detailsHtml;
    
    // Show the modal
    const bsModal = new bootstrap.Modal(modal);
    bsModal.show();
}
