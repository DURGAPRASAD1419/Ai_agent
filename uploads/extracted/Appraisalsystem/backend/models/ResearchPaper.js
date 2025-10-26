const mongoose = require('mongoose');

const researchPaperSchema = new mongoose.Schema({
    title: {
        type: String,
        required: true
    },
    abstract: {
        type: String,
        required: true
    },
    authors: [{
        name: String,
        affiliation: String
    }],
    keywords: [String],
    content: {
        type: String,
        required: true
    },
    extractedFeatures: {
        concepts: [String],
        technicalTerms: [String],
        features: [String]
    },
    uploadedBy: {
        type: mongoose.Schema.Types.ObjectId,
        ref: 'User',
        required: true
    },
    filePath: String,
    uploadDate: {
        type: Date,
        default: Date.now
    }
}, {
    timestamps: true
});

module.exports = mongoose.model('ResearchPaper', researchPaperSchema);
