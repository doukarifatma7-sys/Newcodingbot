import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QMessageBox, 
                               QButtonGroup, QLabel, QWidget, QVBoxLayout)
from PySide6.QtCore import Qt, QFile, QIODevice, QPoint, QRect
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import (QPainter, QPainterPath, QLinearGradient, 
                          QBrush, QColor, QFont, QFontDatabase)


class WaveHeaderWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedHeight(240)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create gradient
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor("#0E1A3D"))
        gradient.setColorAt(0.5, QColor("#1a2d5f"))
        gradient.setColorAt(1, QColor("#0E1A3D"))
        
        # Draw main wave
        path = QPainterPath()
        path.moveTo(0, 100)
        path.cubicTo(self.width()/4, 140, self.width()/2, 60, 3*self.width()/4, 100)
        path.cubicTo(5*self.width()/6, 110, 5.75*self.width()/6, 80, self.width(), 100)
        path.lineTo(self.width(), 0)
        path.lineTo(0, 0)
        path.closeSubpath()
        
        painter.fillPath(path, QBrush(gradient))
        
        # Draw second wave with opacity
        path2 = QPainterPath()
        path2.moveTo(0, 80)
        path2.cubicTo(self.width()/3, 100, 2*self.width()/3, 40, self.width(), 80)
        path2.lineTo(self.width(), 0)
        path2.lineTo(0, 0)
        path2.closeSubpath()
        
        painter.setOpacity(0.5)
        painter.fillPath(path2, QBrush(QColor("#0E1A3D")))
        
        # Draw "sign in" text UNDER the wave (not in the wave)
        painter.setOpacity(1)
        painter.setPen(QColor("#0E1A3D"))  # Blue color
        painter.setBrush(Qt.NoBrush)
        
        # Create font for "sign in" - smaller and different style
        font = QFont("Poppins", 30, QFont.Bold)  # Smaller than SIGN IN title
        painter.setFont(font)
        
        # Position text just below the wave (around y=180)
        text_rect = QRect(0, 150, self.width(), 50)
        painter.drawText(text_rect, Qt.AlignCenter, "Sign in")


class SignInWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Load UI file
        self.load_ui()
        
        # Replace header with custom wave widget (which includes "sign in" text)
        self.replace_header_with_wave()
        
        # Setup fonts
        self.setup_fonts()
        
        # Setup connections
        self.setup_connections()
        
        # Initialize login method
        self.login_method = 'email'
        
        # Mock database
        self.users_db = {
            'email': {
                'user@example.com': {
                    'password': 'password123',
                    'name': 'John Doe',
                    'phone': '+213555123456'
                }
            },
            'phone': {
                '+213555123456': {
                    'name': 'John Doe',
                    'email': 'user@example.com'
                }
            }
        }
        
        # Apply exact CSS styles
        self.apply_exact_styles()
        
        # Remove gray area and set background to white
        self.set_white_background()
        
        # Remove label borders (no borders for labels)
        self.remove_label_borders()
        
        # Hide the big SIGN IN title since we have "sign in" under the wave
        self.ui.titleLabel.setVisible(False)
    
    def load_ui(self):
        """Load the UI file"""
        loader = QUiLoader()
        ui_file = QFile("main.ui")
        
        if not ui_file.open(QIODevice.ReadOnly):
            print("Cannot open UI file")
            sys.exit(-1)
        
        self.ui = loader.load(ui_file)
        ui_file.close()
        
        if not self.ui:
            print("Cannot load UI")
            sys.exit(-1)
        
        # Set the loaded UI as central widget
        self.setCentralWidget(self.ui.centralwidget)
        self.setWindowTitle(self.ui.windowTitle())
        self.setMinimumSize(self.ui.minimumSize())
        self.setMaximumSize(self.ui.maximumSize())
        
        # Set exact text as shown in your image
        self.set_exact_text()
    
    def set_exact_text(self):
        """Set all text to match exactly what's in your image"""
        # Title is now hidden (drawn in wave widget)
        
        # Toggle buttons
        self.ui.emailToggleBtn.setText("Email")
        self.ui.phoneToggleBtn.setText("Phone")
        
        # Labels
        self.ui.emailLabel.setText("Email")
        self.ui.phoneLabel.setText("Phone Number")
        self.ui.passwordLabel.setText("Password")
        
        # Placeholders
        self.ui.emailInput.setPlaceholderText("Write into your email")
        self.ui.phoneInput.setPlaceholderText("Write into your phone number")
        self.ui.passwordInput.setPlaceholderText("Write into your password")
        
        # Links
        self.ui.forgotPasswordLabel.setText(
            '<html><head/><body><p><a href="#"><span style="color:#0e1a3d; text-decoration: underline;">Forget password?</span></a></p></body></html>'
        )
        
        self.ui.signUpLabel.setText(
            '<html><head/><body><p align="center"><span style="color:#0e1a3d;">Don\'t have an account? </span><a href="#"><span style="color:#0e1a3d; text-decoration: underline;">Sign Up</span></a></p></body></html>'
        )
        
        # Button
        self.ui.signInBtn.setText("Sign in")
    
    def replace_header_with_wave(self):
        """Replace the plain header with wave widget"""
        header_widget = self.ui.headerWidget
        
        # Create custom wave widget WITH "sign in" text
        wave_widget = WaveHeaderWidget()
        
        # Replace in layout
        layout = self.ui.verticalLayout
        for i in range(layout.count()):
            widget = layout.itemAt(i).widget()
            if widget == header_widget:
                layout.replaceWidget(header_widget, wave_widget)
                header_widget.deleteLater()
                break
        
        # Store reference
        self.wave_widget = wave_widget
    
    def set_white_background(self):
        """Set all backgrounds to white to remove gray area"""
        # Set main window background to white
        self.setStyleSheet("""
            QMainWindow {
                background-color: white;
            }
            
            QWidget#formWidget {
                background-color: white;
            }
            
            QWidget#emailWidget, QWidget#phoneWidget, QWidget#passwordWidget {
                background-color: white;
            }
            
            QLabel {
                background-color: transparent;
            }
        """)
        
        # Set specific widget backgrounds
        self.ui.formWidget.setStyleSheet("background-color: white;")
        self.ui.emailWidget.setStyleSheet("background-color: white;")
        self.ui.phoneWidget.setStyleSheet("background-color: white;")
        self.ui.passwordWidget.setStyleSheet("background-color: white;")
        
        # Set labels background to transparent
        self.ui.emailLabel.setStyleSheet(self.ui.emailLabel.styleSheet() + "background-color: transparent;")
        self.ui.phoneLabel.setStyleSheet(self.ui.phoneLabel.styleSheet() + "background-color: transparent;")
        self.ui.passwordLabel.setStyleSheet(self.ui.passwordLabel.styleSheet() + "background-color: transparent;")
        self.ui.forgotPasswordLabel.setStyleSheet(self.ui.forgotPasswordLabel.styleSheet() + "background-color: transparent;")
        self.ui.signUpLabel.setStyleSheet(self.ui.signUpLabel.styleSheet() + "background-color: transparent;")
        self.ui.titleLabel.setStyleSheet(self.ui.titleLabel.styleSheet() + "background-color: transparent;")
    
    def remove_label_borders(self):
        """Remove borders from labels - they should be plain text, not bordered boxes"""
        label_style = """
            QLabel {
                color: #0E1A3D;
                font-family: 'Orbitron', sans-serif;
                font-size: 14px;
                margin-bottom: 5px;
                border: none;
                background-color: transparent;
                padding: 0;
            }
        """
        
        # Apply to all form labels (NO borders)
        self.ui.emailLabel.setStyleSheet(label_style)
        self.ui.phoneLabel.setStyleSheet(label_style)
        self.ui.passwordLabel.setStyleSheet(label_style)
    
    def setup_fonts(self):
        """Setup custom fonts"""
        pass
    
    def apply_exact_styles(self):
        """Apply exact CSS styles from the provided CSS file"""
        
        # Update labels font family and size (NO borders)
        label_style = """
            QLabel {
                color: #0E1A3D;
                font-family: 'Orbitron', sans-serif;
                font-size: 14px;
                margin-bottom: 5px;
                border: none;
                background-color: transparent;
                padding: 0;
            }
        """
        
        # Apply to all labels (NO borders)
        self.ui.emailLabel.setStyleSheet(label_style)
        self.ui.phoneLabel.setStyleSheet(label_style)
        self.ui.passwordLabel.setStyleSheet(label_style)
        
        # Update input fields (exact match with CSS)
        input_style = """
            QLineEdit {
                width: 100%;
                padding: 12px 16px;
                border-radius: 8px;
                background-color: white;
                border: 2px solid #0E1A3D;
                color: #0E1A3D;
                font-family: 'Orbitron', sans-serif;
                font-size: 13px;
            }
            
            QLineEdit::placeholder {
                color: rgba(14, 26, 61, 0.5);
            }
            
            QLineEdit:focus {
                border: 3px solid #0E1A3D !important;
                outline: none;
            }
            
            QLineEdit:focus-visible {
                border: 3px solid #0E1A3D !important;
                outline: none;
            }
        """
        
        # Apply input styles
        self.ui.emailInput.setStyleSheet(input_style)
        self.ui.phoneInput.setStyleSheet(input_style)
        self.ui.passwordInput.setStyleSheet(input_style)
        
        # Update toggle buttons (exact match)
        toggle_button_style = """
            QPushButton {
                background-color: white;
                color: #0E1A3D;
                border: 2px solid #0E1A3D;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Orbitron', sans-serif;
                font-weight: 600;
                font-size: 13px;
                transition: all 0.2s ease;
            }
            
            QPushButton:checked {
                background-color: #0E1A3D;
                color: white;
            }
            
            QPushButton:hover {
                 transform: translateY(-1px);
            }
        """
        
        self.ui.emailToggleBtn.setStyleSheet(toggle_button_style)
        self.ui.phoneToggleBtn.setStyleSheet(toggle_button_style)
        
        # Update sign in button with exact shadow and hover effects
        signin_button_style = """
            QPushButton {
                width: 100%;
                padding: 15px 16px;
                border-radius: 8px;
                background-color: #FFD800;
                color: #0E1A3D;
                font-family: 'Orbitron', sans-serif;
                font-weight: 600;
                border: none;
                font-size: 14px;
                transition: all 0.3s ease;
            }
            
            QPushButton:hover {
                background-color: #E6C400;
                transform: translateY(-1px);
            }
            
            QPushButton:pressed {
                transform: translateY(0);
            }
        """
        
        self.ui.signInBtn.setStyleSheet(signin_button_style)
        
        # Update links style
        link_style = """
            QLabel {
                color: #0E1A3D;
                font-size: 13px;
                font-family: 'Orbitron', sans-serif;
                border: none;
                background-color: transparent;
            }
            
            QLabel:hover {
                opacity: 0.8;
            }
        """
        
        self.ui.forgotPasswordLabel.setStyleSheet(link_style)
        self.ui.signUpLabel.setStyleSheet(link_style)
    
    def setup_connections(self):
        """Setup signal/slot connections"""
        # Create button group for toggle buttons
        self.toggle_group = QButtonGroup(self)
        self.toggle_group.addButton(self.ui.emailToggleBtn)
        self.toggle_group.addButton(self.ui.phoneToggleBtn)
        self.toggle_group.setExclusive(True)
        
        # Connect toggle buttons
        self.ui.emailToggleBtn.clicked.connect(self.on_email_toggle)
        self.ui.phoneToggleBtn.clicked.connect(self.on_phone_toggle)
        
        # Connect sign in button
        self.ui.signInBtn.clicked.connect(self.on_sign_in)
        
        # Connect forgot password link
        self.ui.forgotPasswordLabel.linkActivated.connect(self.on_forgot_password)
        
        # Connect sign up link
        self.ui.signUpLabel.linkActivated.connect(self.on_sign_up)
        
        # Connect Enter key press to sign in
        self.ui.emailInput.returnPressed.connect(self.on_sign_in)
        self.ui.phoneInput.returnPressed.connect(self.on_sign_in)
        self.ui.passwordInput.returnPressed.connect(self.on_sign_in)
    
    def on_email_toggle(self):
        """Handle email toggle button click"""
        self.login_method = 'email'
        self.ui.emailWidget.setVisible(True)
        self.ui.phoneWidget.setVisible(False)
        self.ui.passwordWidget.setVisible(True)
    
    def on_phone_toggle(self):
        """Handle phone toggle button click"""
        self.login_method = 'phone'
        self.ui.emailWidget.setVisible(False)
        self.ui.phoneWidget.setVisible(True)
        self.ui.passwordWidget.setVisible(False)
    
    def on_sign_in(self):
        """Handle sign in button click"""
        if self.login_method == 'email':
            email = self.ui.emailInput.text().strip()
            password = self.ui.passwordInput.text()
            
            if not email:
                QMessageBox.warning(self, "Error", "Please enter your email.")
                return
            
            if not password:
                QMessageBox.warning(self, "Error", "Please enter your password.")
                return
            
            if email in self.users_db['email']:
                user = self.users_db['email'][email]
                if user['password'] == password:
                    QMessageBox.information(
                        self, 
                        "Success", 
                        f"Welcome back, {user['name']}!\n\nLogged in with email: {email}"
                    )
                else:
                    QMessageBox.critical(self, "Error", "Invalid password.")
            else:
                QMessageBox.critical(self, "Error", "User not found.")
        
        elif self.login_method == 'phone':
            phone = self.ui.phoneInput.text().strip()
            
            if not phone:
                QMessageBox.warning(self, "Error", "Please enter your phone number.")
                return
            
            if phone in self.users_db['phone']:
                user = self.users_db['phone'][phone]
                QMessageBox.information(
                    self, 
                    "Success", 
                    f"Welcome back, {user['name']}!\n\nLogged in with phone: {phone}"
                )
            else:
                QMessageBox.critical(self, "Error", "Phone number not found.")
    
    def on_forgot_password(self, link):
        """Handle forgot password link click"""
        QMessageBox.information(
            self, 
            "Forgot Password", 
            "Password recovery functionality would be implemented here."
        )
    
    def on_sign_up(self, link):
        """Handle sign up link click"""
        QMessageBox.information(
            self, 
            "Sign Up", 
            "This would open the Sign Up page."
        )


def main():
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show the window
    window = SignInWindow()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()