
namespace SE300_PasswordManager_Mockup
{
    partial class MainForm
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            PasswordViewer_DataGridView = new DataGridView();
            PasswordViewer_Button_Add = new Button();
            PasswordViewer_Button_Settings = new Button();
            ((System.ComponentModel.ISupportInitialize)PasswordViewer_DataGridView).BeginInit();
            SuspendLayout();
            // 
            // PasswordViewer_DataGridView
            // 
            PasswordViewer_DataGridView.ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.AutoSize;
            PasswordViewer_DataGridView.GridColor = SystemColors.Window;
            PasswordViewer_DataGridView.Location = new Point(12, 58);
            PasswordViewer_DataGridView.Name = "PasswordViewer_DataGridView";
            PasswordViewer_DataGridView.RowHeadersWidth = 72;
            PasswordViewer_DataGridView.Size = new Size(776, 380);
            PasswordViewer_DataGridView.TabIndex = 0;
            PasswordViewer_DataGridView.CellContentClick += PasswordViewer_DataGridView_CellContentClick;
            // 
            // PasswordViewer_Button_Add
            // 
            PasswordViewer_Button_Add.Location = new Point(12, 12);
            PasswordViewer_Button_Add.Name = "PasswordViewer_Button_Add";
            PasswordViewer_Button_Add.Size = new Size(131, 40);
            PasswordViewer_Button_Add.TabIndex = 1;
            PasswordViewer_Button_Add.Text = "Add New";
            PasswordViewer_Button_Add.UseVisualStyleBackColor = true;
            PasswordViewer_Button_Add.Click += button1_Click;
            // 
            // PasswordViewer_Button_Settings
            // 
            PasswordViewer_Button_Settings.Location = new Point(149, 12);
            PasswordViewer_Button_Settings.Name = "PasswordViewer_Button_Settings";
            PasswordViewer_Button_Settings.Size = new Size(131, 40);
            PasswordViewer_Button_Settings.TabIndex = 2;
            PasswordViewer_Button_Settings.Text = "Settings";
            PasswordViewer_Button_Settings.UseVisualStyleBackColor = true;
            // 
            // MainForm
            // 
            AutoScaleDimensions = new SizeF(12F, 30F);
            AutoScaleMode = AutoScaleMode.Font;
            ClientSize = new Size(800, 450);
            Controls.Add(PasswordViewer_Button_Settings);
            Controls.Add(PasswordViewer_Button_Add);
            Controls.Add(PasswordViewer_DataGridView);
            Name = "MainForm";
            Text = "Password Viewer";
            Load += Form1_Load;
            ((System.ComponentModel.ISupportInitialize)PasswordViewer_DataGridView).EndInit();
            ResumeLayout(false);
        }

        private DataGridView PasswordViewer_DataGridView;


        #endregion

        private Button PasswordViewer_Button_Add;
        private Button PasswordViewer_Button_Settings;
    }
}
