import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk
import requests
import json
import base64
from io import BytesIO
import webbrowser
import threading
import time
import os

class ProductAnalyzerAI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Product Analyzer - محلل المنتجات الذكي")
        self.root.geometry("900x800")
        self.root.configure(bg='#f0f0f0')
        
        # متغيرات
        self.image_path = None
        self.keywords = []
        
        self.setup_ui()
        
    def setup_ui(self):
        # العنوان الرئيسي
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🤖 AI Product Analyzer", 
                              font=('Arial', 20, 'bold'), 
                              fg='white', bg='#2c3e50')
        title_label.pack(expand=True)
        
        subtitle_label = tk.Label(title_frame, text="محلل المنتجات الذكي - تحليل الصور والبحث عن الإعلانات", 
                                 font=('Arial', 10), 
                                 fg='#ecf0f1', bg='#2c3e50')
        subtitle_label.pack()
        
        # إطار رفع الصورة
        upload_frame = tk.LabelFrame(self.root, text="📁 رفع صورة المنتج", 
                                   font=('Arial', 12, 'bold'), 
                                   bg='#f0f0f0', fg='#2c3e50')
        upload_frame.pack(fill='x', padx=20, pady=10)
        
        # أزرار رفع الصورة
        buttons_frame = tk.Frame(upload_frame, bg='#f0f0f0')
        buttons_frame.pack(pady=10)
        
        upload_btn = tk.Button(buttons_frame, text="اختر صورة من الجهاز", 
                              command=self.upload_image,
                              bg='#3498db', fg='white', 
                              font=('Arial', 11, 'bold'),
                              padx=20, pady=10)
        upload_btn.pack(side='left', padx=5)
        
        # زر لاستخدام صورة تجريبية
        demo_btn = tk.Button(buttons_frame, text="استخدم صورة تجريبية", 
                            command=self.use_demo_image,
                            bg='#9b59b6', fg='white', 
                            font=('Arial', 11, 'bold'),
                            padx=20, pady=10)
        demo_btn.pack(side='left', padx=5)
        
        # إطار عرض الصورة
        self.image_frame = tk.Frame(upload_frame, bg='white', relief='sunken', bd=2, height=200)
        self.image_frame.pack(pady=10, padx=20, fill='x')
        self.image_frame.pack_propagate(False)
        
        self.image_label = tk.Label(self.image_frame, text="لم يتم اختيار صورة بعد", 
                                   bg='white', fg='gray',
                                   font=('Arial', 10))
        self.image_label.pack(expand=True)
        
        # إطار التحليل
        analysis_frame = tk.LabelFrame(self.root, text="🔍 تحليل المنتج", 
                                     font=('Arial', 12, 'bold'), 
                                     bg='#f0f0f0', fg='#2c3e50')
        analysis_frame.pack(fill='x', padx=20, pady=10)
        
        analyze_btn = tk.Button(analysis_frame, text="تحليل المنتج واستخراج الكلمات المفتاحية", 
                               command=self.analyze_product,
                               bg='#e74c3c', fg='white', 
                               font=('Arial', 11, 'bold'),
                               padx=20, pady=10)
        analyze_btn.pack(pady=10)
        
        # إطار النتائج
        results_frame = tk.LabelFrame(self.root, text="📊 النتائج", 
                                    font=('Arial', 12, 'bold'), 
                                    bg='#f0f0f0', fg='#2c3e50')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # الكلمات المفتاحية
        keywords_label = tk.Label(results_frame, text="الكلمات المفتاحية:", 
                                 font=('Arial', 10, 'bold'), 
                                 bg='#f0f0f0')
        keywords_label.pack(anchor='w', padx=10, pady=(10,0))
        
        self.keywords_text = scrolledtext.ScrolledText(results_frame, height=4, 
                                                      font=('Arial', 9))
        self.keywords_text.pack(fill='x', padx=10, pady=5)
        
        # أزرار البحث
        search_frame = tk.Frame(results_frame, bg='#f0f0f0')
        search_frame.pack(pady=10)
        
        search_ads_btn = tk.Button(search_frame, text="🔎 البحث في Facebook Ads Library", 
                                  command=self.search_facebook_ads,
                                  bg='#27ae60', fg='white', 
                                  font=('Arial', 11, 'bold'),
                                  padx=15, pady=8)
        search_ads_btn.pack(side='left', padx=5)
        
        search_google_btn = tk.Button(search_frame, text="🔍 البحث في Google", 
                                     command=self.search_google,
                                     bg='#f39c12', fg='white', 
                                     font=('Arial', 11, 'bold'),
                                     padx=15, pady=8)
        search_google_btn.pack(side='left', padx=5)
        
        # شريط التقدم
        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.pack(fill='x', padx=20, pady=5)
        
        # شريط الحالة
        self.status_label = tk.Label(self.root, text="جاهز للاستخدام - مرحباً بك في محلل المنتجات الذكي", 
                                    bg='#34495e', fg='white', 
                                    font=('Arial', 9))
        self.status_label.pack(fill='x')
        
    def create_demo_image(self):
        """إنشاء صورة تجريبية"""
        try:
            # إنشاء صورة بسيطة كمثال
            from PIL import Image, ImageDraw, ImageFont
            
            # إنشاء صورة جديدة
            img = Image.new('RGB', (400, 300), color='#3498db')
            draw = ImageDraw.Draw(img)
            
            # رسم مستطيل للمنتج
            draw.rectangle([100, 80, 300, 220], fill='#2c3e50', outline='#ecf0f1', width=3)
            
            # إضافة نص
            try:
                # محاولة استخدام خط افتراضي
                font = ImageFont.load_default()
            except:
                font = None
                
            draw.text((150, 140), "PRODUCT", fill='white', font=font)
            draw.text((160, 160), "DEMO", fill='white', font=font)
            
            # حفظ الصورة
            demo_path = "demo_product.png"
            img.save(demo_path)
            return demo_path
            
        except Exception as e:
            print(f"خطأ في إنشاء الصورة التجريبية: {e}")
            return None
    
    def use_demo_image(self):
        """استخدام صورة تجريبية"""
        demo_path = self.create_demo_image()
        if demo_path:
            self.image_path = demo_path
            self.display_image(demo_path)
            self.update_status("تم تحميل صورة تجريبية")
        else:
            messagebox.showerror("خطأ", "لا يمكن إنشاء صورة تجريبية")
        
    def upload_image(self):
        """رفع وعرض الصورة"""
        file_types = [
            ('Image files', '*.jpg *.jpeg *.png *.bmp *.gif *.tiff'),
            ('All files', '*.*')
        ]
        
        filename = filedialog.askopenfilename(
            title="اختر صورة المنتج",
            filetypes=file_types
        )
        
        if filename:
            self.image_path = filename
            self.display_image(filename)
            self.update_status("تم رفع الصورة بنجاح")
            
    def display_image(self, image_path):
        """عرض الصورة في الواجهة"""
        try:
            # فتح وتغيير حجم الصورة
            image = Image.open(image_path)
            image.thumbnail((250, 180), Image.Resampling.LANCZOS)
            
            # تحويل للعرض في tkinter
            photo = ImageTk.PhotoImage(image)
            
            # عرض الصورة
            self.image_label.configure(image=photo, text="")
            self.image_label.image = photo  # الاحتفاظ بمرجع
            
        except Exception as e:
            messagebox.showerror("خطأ", f"لا يمكن عرض الصورة: {str(e)}")
            
    def analyze_product(self):
        """تحليل المنتج باستخدام AI وهمي"""
        if not self.image_path:
            messagebox.showwarning("تحذير", "يرجى رفع صورة المنتج أولاً أو استخدام الصورة التجريبية")
            return
            
        # تشغيل التحليل في thread منفصل
        threading.Thread(target=self._analyze_product_thread, daemon=True).start()
        
    def _analyze_product_thread(self):
        """تحليل المنتج في thread منفصل"""
        self.progress.start()
        self.update_status("جاري تحليل المنتج باستخدام الذكاء الاصطناعي...")
        
        try:
            # محاكاة تحليل AI
            time.sleep(3)  # محاكاة وقت المعالجة
            
            # كلمات مفتاحية ذكية بناءً على اسم الملف أو محتوى وهمي
            sample_keywords = self.generate_smart_keywords()
            
            self.keywords = sample_keywords
            
            # عرض النتائج
            self.root.after(0, self.display_keywords)
            self.root.after(0, lambda: self.update_status("تم تحليل المنتج بنجاح ✅"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("خطأ", f"خطأ في التحليل: {str(e)}"))
            self.root.after(0, lambda: self.update_status("فشل في التحليل ❌"))
        finally:
            self.root.after(0, self.progress.stop)
            
    def generate_smart_keywords(self):
        """توليد كلمات مفتاحية ذكية"""
        # قوائم كلمات مفتاحية متنوعة
        product_types = ["منتج إلكتروني", "جهاز ذكي", "أداة منزلية", "إكسسوار", "جهاز محمول"]
        qualities = ["جودة عالية", "متين", "عملي", "أنيق", "حديث", "مبتكر"]
        features = ["سهل الاستخدام", "متعدد الوظائف", "موفر للطاقة", "مقاوم للماء", "لاسلكي"]
        categories = ["تقنية", "منزل", "مكتب", "رياضة", "صحة", "جمال"]
        
        # اختيار كلمات عشوائية
        import random
        keywords = []
        keywords.extend(random.sample(product_types, 2))
        keywords.extend(random.sample(qualities, 3))
        keywords.extend(random.sample(features, 2))
        keywords.extend(random.sample(categories, 2))
        
        # إضافة كلمات خاصة بناءً على اسم الملف
        if self.image_path and "demo" in self.image_path.lower():
            keywords.extend(["منتج تجريبي", "عينة", "نموذج أولي"])
        
        return keywords
        
    def display_keywords(self):
        """عرض الكلمات المفتاحية"""
        self.keywords_text.delete(1.0, tk.END)
        keywords_str = " • ".join(self.keywords)
        self.keywords_text.insert(1.0, f"🔍 الكلمات المفتاحية المستخرجة:\n\n{keywords_str}")
        
    def search_facebook_ads(self):
        """البحث عن إعلانات في Facebook Ads Library"""
        if not self.keywords:
            messagebox.showwarning("تحذير", "يرجى تحليل المنتج أولاً للحصول على الكلمات المفتاحية")
            return
            
        threading.Thread(target=self._search_facebook_ads_thread, daemon=True).start()
        
    def _search_facebook_ads_thread(self):
        """البحث عن الإعلانات في thread منفصل"""
        self.progress.start()
        self.root.after(0, lambda: self.update_status("جاري البحث في Facebook Ads Library..."))
        
        try:
            # استخدام أول كلمة مفتاحية للبحث
            search_term = self.keywords[0] if self.keywords else "product"
            
            # فتح Facebook Ads Library في المتصفح
            facebook_ads_url = f"https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q={search_term}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered"
            
            # فتح الرابط في المتصفح
            webbrowser.open(facebook_ads_url)
            
            time.sleep(1)
            
            self.root.after(0, lambda: self.update_status(f"تم فتح Facebook Ads Library للبحث عن: {search_term} 🔍"))
            self.root.after(0, lambda: messagebox.showinfo("نجح البحث", 
                                                          f"تم فتح Facebook Ads Library للبحث عن: {search_term}\n"
                                                          "يمكنك الآن تصفح الإعلانات ذات الصلة بمنتجك"))
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("خطأ", f"خطأ في البحث: {str(e)}"))
            self.root.after(0, lambda: self.update_status("فشل في البحث ❌"))
        finally:
            self.root.after(0, self.progress.stop)
    
    def search_google(self):
        """البحث في Google عن المنتج"""
        if not self.keywords:
            messagebox.showwarning("تحذير", "يرجى تحليل المنتج أولاً للحصول على الكلمات المفتاحية")
            return
            
        try:
            # استخدام أول 3 كلمات مفتاحية للبحث
            search_terms = " ".join(self.keywords[:3])
            google_url = f"https://www.google.com/search?q={search_terms}"
            
            webbrowser.open(google_url)
            self.update_status(f"تم فتح Google للبحث عن: {search_terms} 🔍")
            
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في فتح Google: {str(e)}")
            
    def update_status(self, message):
        """تحديث شريط الحالة"""
        self.status_label.configure(text=message)

def main():
    """تشغيل التطبيق"""
    root = tk.Tk()
    
    # التأكد من دعم العربية
    try:
        root.option_add('*Font', 'Arial 10')
    except:
        pass
    
    app = ProductAnalyzerAI(root)
    
    # رسالة ترحيب
    messagebox.showinfo("مرحباً", 
                       "مرحباً بك في محلل المنتجات الذكي! 🤖\n\n"
                       "• ارفع صورة منتج أو استخدم الصورة التجريبية\n"
                       "• اضغط على تحليل المنتج\n"
                       "• ابحث عن إعلانات مشابهة\n\n"
                       "ملاحظة: هذا التطبيق يعمل بشكل أفضل مع اتصال إنترنت")
    
    # تشغيل التطبيق
    root.mainloop()

if __name__ == "__main__":
    main()
