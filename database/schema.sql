-- =====================================================
-- Zero Waste AI Platform - Database Schema
-- MySQL Database
-- =====================================================

-- Create database (run this separately if needed)
-- CREATE DATABASE IF NOT EXISTS waste_management;
-- USE waste_management;

-- =====================================================
-- Users Table
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200),
    bio TEXT,
    role ENUM('user', 'moderator', 'admin') DEFAULT 'user',
    points INT DEFAULT 0,
    profile_image VARCHAR(500),
    is_active BOOLEAN DEFAULT TRUE,
    last_login DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_points (points)
);

-- =====================================================
-- Waste Records Table
-- =====================================================
CREATE TABLE IF NOT EXISTS waste_records (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    waste_type VARCHAR(50) NOT NULL,
    waste_subtype VARCHAR(100),
    quantity_kg DECIMAL(10,2) DEFAULT 0,
    disposal_method VARCHAR(100),
    recyclable BOOLEAN DEFAULT TRUE,
    confidence_score DECIMAL(5,2),
    image_path VARCHAR(500),
    description TEXT,
    points_earned INT DEFAULT 0,
    date_recorded DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_waste_type (waste_type),
    INDEX idx_date (date_recorded),
    INDEX idx_recyclable (recyclable)
);

-- =====================================================
-- Chemical Reactions Table (Atom Economy)
-- =====================================================
CREATE TABLE IF NOT EXISTS chemical_reactions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    reaction_name VARCHAR(200),
    reactants TEXT,
    products TEXT,
    reactants_weight DECIMAL(10,2),
    products_weight DECIMAL(10,2),
    atom_economy DECIMAL(5,2),
    efficiency_rating ENUM('Excellent', 'Good', 'Average', 'Poor'),
    solvent_used VARCHAR(100),
    catalyst VARCHAR(100),
    temperature INT,
    reaction_time INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_atom_economy (atom_economy)
);

-- =====================================================
-- Green Solvents Database
-- =====================================================
CREATE TABLE IF NOT EXISTS green_solvents (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    green_rating ENUM('Excellent', 'Very Good', 'Good', 'Moderate') DEFAULT 'Good',
    applications TEXT,
    toxicity ENUM('Non-toxic', 'Low', 'Moderate', 'High') DEFAULT 'Low',
    boiling_point DECIMAL(8,2),
    density DECIMAL(8,4),
    biodegradability BOOLEAN DEFAULT TRUE,
    renewable_source BOOLEAN DEFAULT FALSE,
    cost_rating ENUM('Low', 'Medium', 'High') DEFAULT 'Medium',
    INDEX idx_rating (green_rating)
);

-- =====================================================
-- Tutorials Table
-- =====================================================
CREATE TABLE IF NOT EXISTS tutorials (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(200) NOT NULL,
    content LONGTEXT NOT NULL,
    category VARCHAR(50) NOT NULL,
    tags VARCHAR(500),
    thumbnail VARCHAR(500),
    author_id INT NOT NULL,
    status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
    views INT DEFAULT 0,
    likes INT DEFAULT 0,
    approved_by INT,
    approved_at DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (approved_by) REFERENCES users(id),
    INDEX idx_status (status),
    INDEX idx_category (category),
    INDEX idx_views (views)
);

-- =====================================================
-- Tutorial Comments Table
-- =====================================================
CREATE TABLE IF NOT EXISTS tutorial_comments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tutorial_id INT NOT NULL,
    user_id INT NOT NULL,
    comment TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (tutorial_id) REFERENCES tutorials(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_tutorial_id (tutorial_id)
);

-- =====================================================
-- Badges Table
-- =====================================================
CREATE TABLE IF NOT EXISTS badges (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    color VARCHAR(20),
    points_required INT DEFAULT 0,
    waste_recycled_required DECIMAL(10,2) DEFAULT 0,
    INDEX idx_points (points_required)
);

-- =====================================================
-- User Badges Table
-- =====================================================
CREATE TABLE IF NOT EXISTS user_badges (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    badge_id INT NOT NULL,
    earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (badge_id) REFERENCES badges(id) ON DELETE CASCADE,
    UNIQUE KEY unique_user_badge (user_id, badge_id),
    INDEX idx_user_id (user_id)
);

-- =====================================================
-- User Activity Log
-- =====================================================
CREATE TABLE IF NOT EXISTS user_activity (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    activity_type VARCHAR(50) NOT NULL,
    description TEXT,
    points_earned INT DEFAULT 0,
    ip_address VARCHAR(45),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_activity_type (activity_type),
    INDEX idx_created_at (created_at)
);

-- =====================================================
-- Reports Table
-- =====================================================
CREATE TABLE IF NOT EXISTS reports (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    report_type VARCHAR(50) NOT NULL,
    report_name VARCHAR(200),
    file_path VARCHAR(500),
    file_size INT,
    date_range_start DATE,
    date_range_end DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id)
);

-- =====================================================
-- Waste Prediction Models Data
-- =====================================================
CREATE TABLE IF NOT EXISTS waste_predictions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    population INT,
    households INT,
    area_type VARCHAR(50),
    predicted_daily_waste DECIMAL(10,2),
    predicted_weekly_waste DECIMAL(10,2),
    predicted_monthly_waste DECIMAL(10,2),
    confidence_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_user_id (user_id)
);

-- =====================================================
-- Insert Initial Data - Badges
-- =====================================================
INSERT INTO badges (name, description, icon, color, points_required, waste_recycled_required) VALUES
('Recycler', 'Recycled 100 kg of waste', 'recycle', 'success', 0, 100),
('Chemist', 'Performed 50 atom economy calculations', 'flask', 'info', 50, 0),
('Eco Warrior', 'Earned 500 points', 'leaf', 'warning', 500, 0),
('Contributor', 'Submitted approved tutorial', 'pen-fancy', 'primary', 0, 0),
('Green Solvent Expert', 'Recommended 10 green solvents', 'droplet', 'success', 0, 0),
('Zero Waste Hero', 'Achieved 90% recycling rate', 'trophy', 'gold', 1000, 500);

-- =====================================================
-- Insert Initial Data - Green Solvents
-- =====================================================
INSERT INTO green_solvents (name, green_rating, applications, toxicity, boiling_point, density, biodegradability, renewable_source, cost_rating) VALUES
('Water', 'Excellent', 'Many organic reactions, Cleaning', 'Non-toxic', 100.00, 1.0000, TRUE, TRUE, 'Low'),
('Ethanol', 'Excellent', 'Extractions, Synthesis', 'Low', 78.37, 0.7890, TRUE, TRUE, 'Low'),
('Isopropyl Alcohol', 'Good', 'Cleaning, Extractions', 'Low', 82.60, 0.7860, TRUE, FALSE, 'Low'),
('Ethyl Acetate', 'Good', 'Chromatography, Extractions', 'Low', 77.10, 0.9020, TRUE, FALSE, 'Medium'),
('Supercritical CO₂', 'Excellent', 'Extractions, Dry cleaning', 'Non-toxic', 31.00, 0.4700, TRUE, TRUE, 'High'),
('Glycerol', 'Excellent', 'Solvent, Plasticizer', 'Non-toxic', 290.00, 1.2610, TRUE, TRUE, 'Low'),
('Dimethyl Carbonate', 'Good', 'Methylation, Solvent', 'Low', 90.00, 1.0700, TRUE, TRUE, 'Medium'),
('2-Methyltetrahydrofuran', 'Very Good', 'Grignard reactions, Organometallic', 'Moderate', 80.00, 0.8600, TRUE, TRUE, 'Medium');

-- =====================================================
-- Insert Initial Data - Sample Tutorials
-- =====================================================
INSERT INTO tutorials (title, content, category, tags, author_id, status, views, likes) VALUES
('Introduction to Zero Waste Living', 'Zero waste living is a philosophy that encourages the redesign of resource life cycles so that all products are reused. The goal is for no trash to be sent to landfills, incinerators, or the ocean...', 'zero-waste', 'sustainable, lifestyle, tips', 1, 'approved', 1250, 85),
('Home Composting Guide', 'Composting is a natural process that turns organic materials into a nutrient-rich soil amendment. This guide will help you start composting at home...', 'composting', 'compost, organic, garden', 1, 'approved', 890, 67),
('Understanding Atom Economy', 'Atom economy is a measure of the efficiency of a chemical reaction. It is calculated by dividing the molecular weight of the desired products by the molecular weight of all reactants...', 'green-chemistry', 'chemistry, efficiency, green', 1, 'approved', 650, 42),
('Plastic Recycling: What You Need to Know', 'Not all plastics are created equal. Learn which plastics can be recycled and how to prepare them for recycling...', 'recycling', 'plastic, recycle, environment', 1, 'approved', 2100, 156),
('E-Waste Management Guide', 'Electronic waste is one of the fastest-growing waste streams. Learn how to properly dispose of your electronic devices...', 'e-waste', 'electronics, recycling, hazardous', 1, 'approved', 720, 51);

-- =====================================================
-- Insert Initial Data - Demo User (password: demo123)
-- =====================================================
-- Note: Password hash is for 'demo123' - in production use proper hashing
INSERT INTO users (username, email, password_hash, role, points, is_active) VALUES
('demo_user', 'demo@example.com', '5f4dcc3b5aa765d61d8327deb882cf99', 'user', 150, TRUE),
('admin', 'admin@example.com', '5f4dcc3b5aa765d61d8327deb882cf99', 'admin', 500, TRUE),
('moderator', 'mod@example.com', '5f4dcc3b5aa765d61d8327deb882cf99', 'moderator', 250, TRUE);

-- =====================================================
-- Views for Analytics
-- =====================================================

-- View: User Summary
CREATE OR REPLACE VIEW user_summary AS
SELECT 
    u.id,
    u.username,
    u.email,
    u.role,
    u.points,
    COUNT(DISTINCT wr.id) as total_waste_items,
    COALESCE(SUM(wr.quantity_kg), 0) as total_waste_recycled,
    COUNT(DISTINCT cr.id) as total_calculations,
    COUNT(DISTINCT t.id) as total_tutorials,
    COUNT(DISTINCT ub.id) as total_badges
FROM users u
LEFT JOIN waste_records wr ON u.id = wr.user_id
LEFT JOIN chemical_reactions cr ON u.id = cr.user_id
LEFT JOIN tutorials t ON u.id = t.author_id AND t.status = 'approved'
LEFT JOIN user_badges ub ON u.id = ub.user_id
WHERE u.is_active = TRUE
GROUP BY u.id;

-- View: Waste Statistics by Month
CREATE OR REPLACE VIEW waste_stats_monthly AS
SELECT 
    DATE_FORMAT(date_recorded, '%Y-%m') as month,
    waste_type,
    COUNT(*) as count,
    SUM(quantity_kg) as total_kg,
    SUM(CASE WHEN recyclable = TRUE THEN quantity_kg ELSE 0 END) as recyclable_kg
FROM waste_records
GROUP BY DATE_FORMAT(date_recorded, '%Y-%m'), waste_type
ORDER BY month DESC;

-- =====================================================
-- Stored Procedure: Award Points to User
-- =====================================================
DELIMITER //

CREATE PROCEDURE award_points(
    IN p_user_id INT,
    IN p_points INT,
    IN p_activity_type VARCHAR(50),
    IN p_description TEXT
)
BEGIN
    -- Update user points
    UPDATE users SET points = points + p_points WHERE id = p_user_id;
    
    -- Log activity
    INSERT INTO user_activity (user_id, activity_type, description, points_earned)
    VALUES (p_user_id, p_activity_type, p_description, p_points);
    
    -- Check and award badges
    DECLARE user_points INT;
    DECLARE user_waste DECIMAL(10,2);
    
    SELECT points INTO user_points FROM users WHERE id = p_user_id;
    SELECT COALESCE(SUM(quantity_kg), 0) INTO user_waste FROM waste_records WHERE user_id = p_user_id;
    
    -- Award Eco Warrior badge (500 points)
    IF user_points >= 500 THEN
        INSERT IGNORE INTO user_badges (user_id, badge_id) 
        SELECT p_user_id, id FROM badges WHERE points_required <= 500 LIMIT 1;
    END IF;
    
    -- Award Recycler badge (100 kg waste)
    IF user_waste >= 100 THEN
        INSERT IGNORE INTO user_badges (user_id, badge_id) 
        SELECT p_user_id, id FROM badges WHERE waste_recycled_required <= 100 LIMIT 1;
    END IF;
END //

DELIMITER ;

-- =====================================================
-- Indexes for Performance
-- =====================================================

-- Additional indexes for common queries
CREATE INDEX idx_waste_records_date_user ON waste_records(date_recorded, user_id);
CREATE INDEX idx_tutorials_status_created ON tutorials(status, created_at);
CREATE INDEX idx_activity_user_date ON user_activity(user_id, created_at);
CREATE INDEX idx_reports_user_created ON reports(user_id, created_at);

-- Full-text indexes for search
ALTER TABLE tutorials ADD FULLTEXT INDEX ft_tutorial_title_content (title, content);
ALTER TABLE green_solvents ADD FULLTEXT INDEX ft_solvent_name_app (name, applications);

-- =====================================================
-- End of Schema
-- =====================================================