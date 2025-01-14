from django.core.validators import FileExtensionValidator
from django.db import models
from django.urls import reverse
from convention import settings
from profiles.models import Association, Profile
from profiles.views_utils import get_request_user_profile
from .models_utils import get_related_posts_queryset
import colorsys
from django.utils.timezone import localtime


class Feedback(models.Model):
    """
    Model to store feedbacks
    """
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="feedbacks")
    content = models.TextField(max_length=1000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    treated = models.BooleanField(default=False)

    def __str__(self):
                
        if self.treated:
            suffix = "[Traité]"
        else:
            suffix = "[Non traité]"
            
        created_date = localtime(self.created).strftime("%d/%m/%Y")
            
        return f"{suffix} {str(self.content)} ({created_date})"


class Choice(models.Model):
    """
    Model to store dynamic Choice for themes
    """
    theme_name = models.CharField(max_length=30, unique=True)
    color = models.CharField(max_length=7, default='#000000')
    parent_categorie = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    image = models.ImageField(
        blank=True,
        default='generic_theme.jpg',
        upload_to="themes",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )

    def __str__(self):
        if self.parent_categorie:
            return f"{self.parent_categorie} / {self.theme_name}"

        return self.theme_name

# Choice.objects.get_or_create(theme_name='aucun')


class PostManager(models.Manager):
    def get_related_posts(self, user):
        profile = get_request_user_profile(user)
        friends = profile.friends.all()
        following = profile.following.all()

        related_posts = get_related_posts_queryset(profile, friends, following)

        return related_posts

    def only_posts(self):
        return self.get_queryset().filter(is_post=True)

    def order_by_report_number(self):
        return self.get_queryset().annotate(report_count=models.Count('reported')).order_by('-report_count')


    def order_by_score_pondere(self):
        all_posts = Post.objects.filter(is_post=True)
        return sorted(all_posts, key=lambda post: post.score_pondere, reverse=True)

    def order_by_progress(self):
        all_posts = Post.objects.filter(is_post=True)
        return sorted(all_posts, key=lambda post: post.progress, reverse=True)
     

    def get_all_favorite_posts(self, user):
        profile = get_request_user_profile(user)
        like_objects = Like.objects.filter(profile=profile)
        return [like_object.post for like_object in like_objects]

    def order_by_voter_number(self):
        all_posts = Post.objects.filter(is_post=True)
        return sorted(all_posts, key=lambda post: post.voter_number, reverse=True)

    def get_power_from_user(self, user):
        profile = get_request_user_profile(user)
        power_objects = Power.objects.filter(profile=profile, post=self)

        return power_objects


class Post(models.Model):
    """
    This model is used to show results in main.html
    """

    title = models.TextField(max_length=100, blank=True)
    content = models.TextField(max_length=1000, blank=True)
    is_post = models.BooleanField(default=True)
    is_troll = models.BooleanField(default=False)

    theme = models.ForeignKey(Choice, on_delete=models.SET_NULL, null=True, blank=True)
    # Campus parmis Saclay, Rennes et Metz
    CAMPUS_CHOICES = [('--', '--'), ('Saclay', 'Saclay'), ('Rennes', 'Rennes'), ('Metz', 'Metz')]
    campus = models.CharField(max_length=10, choices=CAMPUS_CHOICES, default='Saclay')
    
    association = models.ForeignKey(Association, on_delete=models.SET_NULL, null=True, blank=True)

    image = models.ImageField(
        blank=True,
        upload_to="posts",
        validators=[FileExtensionValidator(["png", "jpg", "jpeg"])],
    )
    liked = models.ManyToManyField(Profile, blank=True, related_name="likes")
    powered = models.ManyToManyField(Profile, blank=True, related_name="powers")
    reported = models.ManyToManyField(Profile, blank=True, related_name="reports")

    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="posts")

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    # A comment is now seen as a response to a post
    in_response_to = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)

    @property
    def number_comments(self):
        if len(Post.objects.filter(in_response_to=self)) == 0:
            return 0
        res = len(Post.objects.filter(in_response_to=self))
        for comment in Post.objects.filter(in_response_to=self):
            res += comment.number_comments
        return res

    @property
    def report_number(self):
        return self.reported.all().count()

    @property
    def comment_like_number(self):
        # Seulement pour les commentaires
        if not self.is_post:
            # On compte le nombre de power reçu qui valent "1"
            power_like_objects = Power.objects.filter(post=self, power='1')
            return len(power_like_objects)

    @property
    def comment_dislike_number(self):
        # Seulement pour les commentaires
        if not self.is_post:
            # On compte le nombre de power reçu qui valent "0"
            power_dislike_objects = Power.objects.filter(post=self, power='0')
            return len(power_dislike_objects)

    objects = PostManager()

    def __str__(self):
        
        if self.is_post:
            return f"{str(self.title)}"
        
        if len(str(self.content)) > 50:
            return f"{str(self.content)[:50].strip()}.."
        return f"{str(self.content)}"

    @property
    def voter_number(self):
        all_power_objects = Power.objects.filter(post=self)
        return len(all_power_objects)

    @property
    def get_all_power(self):

        all_power_objects = Power.objects.filter(post=self)

        total_power = sum([int(power_object.power) for power_object in all_power_objects])

        return total_power if total_power else 0

    @property
    def get_max_power(self):
        all_power_objects = Power.objects.filter(post=self)

        return len(all_power_objects) * 4

    @property
    def progress(self):
        if not self.get_max_power:
            return 0

        return round((self.get_all_power / self.get_max_power) * 100, 1)

    @property
    def get_color_progress(self):
        hue = self.progress / 100
        # Convertir la teinte en une couleur RVB
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)

        # Convertir les valeurs RVB en valeurs entières de 0 à 255
        rgb_int = tuple(int(x * 255) for x in rgb)

        rgb_int = (int((1 - hue) * 255), int(hue * 255), int(hue * 255 * 0.5))

        # Formater la couleur en format CSS (chaîne hexadécimale)
        color_hex = "#{:02x}{:02x}{:02x}".format(*rgb_int)

        return color_hex

    @property
    def can_be_modified(self):
        TEMPS_MODIFICATION_POSSIBLE = 5 * 60     # 5 minutes
        return (localtime() - self.created).seconds < TEMPS_MODIFICATION_POSSIBLE

    @property
    def n_days_created(self):
        return (localtime() - self.created).days

    @property
    def score_pondere(self):
        
        if self.is_post:
            PONDERATION_NOUVEAUTE_COOL = 200
            return PONDERATION_NOUVEAUTE_COOL/(self.n_days_created+1) + self.voter_number - 300*(self.is_troll)

        # Si c'est un commentaire 
        PONDERATION_NOUVEAUTE_COOL = 5
        return PONDERATION_NOUVEAUTE_COOL/(self.n_days_created+1) + self.comment_like_number - 10*(self.is_troll)
    
    
    @property
    def get_absolute_url(self):
        relative_url = reverse("posts:one-post-view", kwargs={"pk": self.pk})[1:] # On enlève le premier "/"
        return settings.BASE_URL + relative_url
    
    @property
    def comments(self):
        # On récupère les commentaires en réponse à ce post trié par score_pondere
        response_comments = Post.objects.filter(in_response_to=self)
        return sorted(response_comments, key=lambda post: post.score_pondere, reverse=True)
    
    class Meta:
        ordering = ("-created",)


class Like(models.Model):
    """
    This model is used to leave likes on Posts
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    puissance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.profile} liked {self.post}"


class Report(models.Model):
    """
    This model is used to leave likes on Posts
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile} reported {self.post}"


class Power(models.Model):
    """
    This model is used to leave power on Posts
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    power = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return f"{self.profile} put {self.power}/5 on {self.post}"
